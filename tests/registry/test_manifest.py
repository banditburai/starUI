"""Tests for manifest tracking."""

import json

import pytest

from starui.registry.checksum import compute_checksum
from starui.registry.manifest import Manifest


@pytest.fixture
def manifest(tmp_path):
    """Create a Manifest rooted at tmp_path."""
    return Manifest(tmp_path)


class TestManifestBasics:
    """Test basic manifest operations."""

    def test_default_state(self, manifest):
        """New manifest starts empty with default registry version."""
        assert manifest.registry_version == "main"
        assert manifest.get_installed() == {}
        assert not manifest.exists()

    def test_record_and_save(self, manifest, tmp_path):
        """record_install is memory-only until save() is called."""
        manifest.record_install("button", version="0.3.0", checksum="sha256:abc", file_path="components/ui/button.py")

        # Not persisted yet
        assert not manifest.exists()

        manifest.save()
        assert manifest.exists()

        # Reload from disk
        fresh = Manifest(tmp_path)
        installed = fresh.get_installed()
        assert "button" in installed
        assert installed["button"]["version"] == "0.3.0"
        assert installed["button"]["checksum"] == "sha256:abc"
        assert installed["button"]["file"] == "components/ui/button.py"

    def test_batch_record_and_save(self, manifest, tmp_path):
        """Multiple record_install calls, single save."""
        manifest.record_install("utils", version="0.3.0", checksum="sha256:aaa", file_path="components/ui/utils.py")
        manifest.record_install("button", version="0.3.0", checksum="sha256:bbb", file_path="components/ui/button.py")
        manifest.record_install("dialog", version="0.3.0", checksum="sha256:ccc", file_path="components/ui/dialog.py")

        manifest.save()

        fresh = Manifest(tmp_path)
        installed = fresh.get_installed()
        assert len(installed) == 3
        assert set(installed.keys()) == {"utils", "button", "dialog"}


class TestManifestAtomicWrites:
    """Test atomic write behavior."""

    def test_save_creates_directory(self, tmp_path):
        """save() creates .starui/ directory if it doesn't exist."""
        manifest = Manifest(tmp_path)
        assert not (tmp_path / ".starui").exists()

        manifest.record_install("x", version="1", checksum="c", file_path="f")
        manifest.save()

        assert (tmp_path / ".starui").is_dir()
        assert (tmp_path / ".starui" / "manifest.json").exists()

    def test_save_is_valid_json(self, manifest, tmp_path):
        """Saved manifest is valid JSON."""
        manifest.record_install("button", version="0.3.0", checksum="sha256:abc", file_path="x.py")
        manifest.save()

        content = (tmp_path / ".starui" / "manifest.json").read_text()
        data = json.loads(content)
        assert "components" in data
        assert "registry_version" in data

    def test_save_no_temp_files_left(self, manifest, tmp_path):
        """No .tmp files left after save."""
        manifest.record_install("button", version="1", checksum="c", file_path="f")
        manifest.save()

        tmp_files = list((tmp_path / ".starui").glob("*.tmp"))
        assert tmp_files == []


class TestManifestIsModified:
    """Test local modification detection."""

    def test_not_modified_when_not_installed(self, manifest, tmp_path):
        """is_modified returns False for unknown components."""
        assert not manifest.is_modified("unknown", tmp_path)

    def test_modified_when_file_missing(self, manifest, tmp_path):
        """is_modified returns True if the local file is gone."""
        manifest.record_install("button", version="1", checksum="sha256:abc", file_path="button.py")
        manifest.save()
        assert manifest.is_modified("button", tmp_path)

    def test_not_modified_when_checksum_matches(self, manifest, tmp_path):
        """is_modified returns False when local file matches recorded checksum."""
        comp_file = tmp_path / "button.py"
        comp_file.write_text("def Button(): pass\n")
        checksum = compute_checksum(comp_file)

        manifest.record_install("button", version="1", checksum=checksum, file_path="button.py")
        manifest.save()

        assert not manifest.is_modified("button", tmp_path)

    def test_modified_when_content_changed(self, manifest, tmp_path):
        """is_modified returns True when local file differs from recorded."""
        comp_file = tmp_path / "button.py"
        comp_file.write_text("def Button(): pass\n")
        checksum = compute_checksum(comp_file)

        manifest.record_install("button", version="1", checksum=checksum, file_path="button.py")
        manifest.save()

        # Modify the file
        comp_file.write_text("def Button(): return 'modified'\n")
        assert manifest.is_modified("button", tmp_path)

    def test_uses_recorded_file_path_not_name(self, manifest, tmp_path):
        """is_modified uses the recorded file path, not hardcoded {name}.py."""
        # Install at a subdirectory path (e.g. components/ui/button.py)
        sub_dir = tmp_path / "components" / "ui"
        sub_dir.mkdir(parents=True)
        comp_file = sub_dir / "button.py"
        comp_file.write_text("def Button(): pass\n")
        checksum = compute_checksum(comp_file)

        manifest.record_install(
            "button",
            version="1",
            checksum=checksum,
            file_path="components/ui/button.py",
        )
        manifest.save()

        # Should find the file at the recorded path, not at component_dir/button.py
        assert not manifest.is_modified("button", tmp_path)

        # Modify it
        comp_file.write_text("def Button(): return 'custom'\n")
        # Reload manifest to clear in-memory cache
        fresh = Manifest(tmp_path)
        assert fresh.is_modified("button", tmp_path)


class TestManifestCorruptedFile:
    """Test handling of corrupted manifest files."""

    def test_corrupted_json_loads_default(self, tmp_path):
        """Corrupted manifest.json falls back to defaults."""
        manifest_dir = tmp_path / ".starui"
        manifest_dir.mkdir()
        (manifest_dir / "manifest.json").write_text("not valid json{{{")

        manifest = Manifest(tmp_path)
        assert manifest.registry_version == "main"
        assert manifest.get_installed() == {}

    def test_empty_file_loads_default(self, tmp_path):
        """Empty manifest.json falls back to defaults."""
        manifest_dir = tmp_path / ".starui"
        manifest_dir.mkdir()
        (manifest_dir / "manifest.json").write_text("")

        manifest = Manifest(tmp_path)
        assert manifest.get_installed() == {}


class TestManifestOverwrite:
    """Test overwriting existing records."""

    def test_overwrite_updates_version_and_checksum(self, manifest, tmp_path):
        """Recording the same component again overwrites the previous record."""
        manifest.record_install("button", version="0.2.0", checksum="sha256:old", file_path="button.py")
        manifest.record_install("button", version="0.3.0", checksum="sha256:new", file_path="button.py")
        manifest.save()

        fresh = Manifest(tmp_path)
        installed = fresh.get_installed()
        assert installed["button"]["version"] == "0.3.0"
        assert installed["button"]["checksum"] == "sha256:new"

    def test_save_empty_manifest(self, manifest, tmp_path):
        """Saving a manifest with no records creates a valid file."""
        manifest.save()

        fresh = Manifest(tmp_path)
        assert fresh.exists()
        assert fresh.get_installed() == {}
        assert fresh.registry_version == "main"


class TestComputeChecksum:
    """Test checksum computation."""

    def test_checksum_format(self, tmp_path):
        """Checksum has sha256: prefix."""
        f = tmp_path / "test.py"
        f.write_text("hello")
        result = compute_checksum(f)
        assert result.startswith("sha256:")
        assert len(result) == 7 + 64  # prefix + hex digest

    def test_checksum_deterministic(self, tmp_path):
        """Same content produces same checksum."""
        f = tmp_path / "test.py"
        f.write_text("hello world")
        c1 = compute_checksum(f)
        c2 = compute_checksum(f)
        assert c1 == c2

    def test_different_content_different_checksum(self, tmp_path):
        """Different content produces different checksums."""
        f1 = tmp_path / "a.py"
        f2 = tmp_path / "b.py"
        f1.write_text("hello")
        f2.write_text("world")
        assert compute_checksum(f1) != compute_checksum(f2)
