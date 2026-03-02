import json
import time
from unittest.mock import MagicMock, patch

import pytest
import requests

from starui.registry.checksum import compute_checksum
from starui.registry.client import INDEX_TTL_SECONDS, RegistryClient

from .conftest import make_component_entry

BUTTON_SOURCE = "def Button(): pass\n"
BUTTON_CHECKSUM = compute_checksum(BUTTON_SOURCE)

TEST_INDEX = {
    "version": "0.3.0",
    "schema_version": 1,
    "components": {
        "utils": make_component_entry("utils", "def cn(): pass\n"),
        "button": make_component_entry("button", BUTTON_SOURCE, deps=["utils"]),
    },
}

TEST_INDEX_TEXT = json.dumps(TEST_INDEX)


@pytest.fixture
def home_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    return tmp_path


def _make_response(text, status=200):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status
    resp.text = text
    resp.raise_for_status = MagicMock()
    if status >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(response=resp)
    return resp


class TestFreshFetch:
    @patch("requests.get")
    def test_fetches_index_from_github(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client = RegistryClient(version="main")
        components = client.list_components()

        assert "button" in components
        assert "utils" not in components

        cache_dir = home_dir / ".starui" / "cache" / "registry" / "main"
        assert (cache_dir / "index.json").exists()
        cached = json.loads((cache_dir / "index.json").read_text())
        assert cached["components"]["button"]["name"] == "button"
        assert (cache_dir / "index.meta.json").exists()

    @patch("requests.get")
    def test_fetches_component_source_and_caches(self, mock_get, home_dir):
        mock_get.side_effect = [
            _make_response(TEST_INDEX_TEXT),
            _make_response(BUTTON_SOURCE),
        ]

        client = RegistryClient(version="main")
        source = client.get_component_source("button")

        assert source == BUTTON_SOURCE
        cached_file = home_dir / ".starui" / "cache" / "registry" / "main" / "components" / "button.py"
        assert cached_file.exists()
        assert cached_file.read_bytes().decode("utf-8") == BUTTON_SOURCE

    @patch("requests.get")
    def test_list_components_returns_sorted_without_utils(self, mock_get, home_dir):
        multi_index = {
            **TEST_INDEX,
            "components": {
                **TEST_INDEX["components"],
                "dialog": make_component_entry("dialog", "def Dialog(): pass\n"),
                "alert": make_component_entry("alert", "def Alert(): pass\n"),
            },
        }
        mock_get.return_value = _make_response(json.dumps(multi_index))

        client = RegistryClient(version="main")
        result = client.list_components()

        assert result == ["alert", "button", "dialog"]
        assert "utils" not in result

    @patch("requests.get")
    def test_get_metadata_returns_component_dict(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client = RegistryClient(version="main")
        meta = client.get_component_metadata("button")

        assert meta["name"] == "button"
        assert meta["dependencies"] == ["utils"]
        assert meta["checksum"] == BUTTON_CHECKSUM

    @patch("requests.get")
    def test_nonexistent_component_raises(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client = RegistryClient(version="main")
        with pytest.raises(FileNotFoundError, match="not found in registry"):
            client.get_component_source("nonexistent")

    @patch("requests.get")
    def test_nonexistent_metadata_raises(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client = RegistryClient(version="main")
        with pytest.raises(FileNotFoundError, match="not found in registry"):
            client.get_component_metadata("nonexistent")


class TestCacheTTL:
    @patch("requests.get")
    def test_fresh_cache_avoids_network(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client1 = RegistryClient(version="main")
        client1.list_components()
        assert mock_get.call_count == 1

        client2 = RegistryClient(version="main")
        components = client2.list_components()
        assert "button" in components
        assert mock_get.call_count == 1

    @patch("requests.get")
    def test_expired_cache_refetches(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client1 = RegistryClient(version="main")
        client1.list_components()

        meta_path = home_dir / ".starui" / "cache" / "registry" / "main" / "index.meta.json"
        expired_time = time.time() - INDEX_TTL_SECONDS - 100
        meta_path.write_text(json.dumps({"fetched_at": expired_time}))

        client2 = RegistryClient(version="main")
        client2.list_components()
        assert mock_get.call_count == 2

    @patch("requests.get")
    def test_expired_cache_falls_back_on_network_error(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)
        client1 = RegistryClient(version="main")
        client1.list_components()

        meta_path = home_dir / ".starui" / "cache" / "registry" / "main" / "index.meta.json"
        expired_time = time.time() - INDEX_TTL_SECONDS - 100
        meta_path.write_text(json.dumps({"fetched_at": expired_time}))

        mock_get.side_effect = requests.ConnectionError("offline")

        client2 = RegistryClient(version="main")
        components = client2.list_components()
        assert "button" in components


class TestImmutableVersions:
    @patch("requests.get")
    def test_tagged_version_cache_never_expires(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client1 = RegistryClient(version="v0.3.0")
        client1.list_components()
        assert mock_get.call_count == 1

        meta_path = home_dir / ".starui" / "cache" / "registry" / "v0.3.0" / "index.meta.json"
        if meta_path.exists():
            meta_path.unlink()

        client2 = RegistryClient(version="v0.3.0")
        components = client2.list_components()
        assert "button" in components
        assert mock_get.call_count == 1

    @patch("requests.get")
    def test_main_branch_is_not_immutable(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client1 = RegistryClient(version="main")
        client1.list_components()

        meta_path = home_dir / ".starui" / "cache" / "registry" / "main" / "index.meta.json"
        meta_path.unlink()

        client2 = RegistryClient(version="main")
        client2.list_components()
        assert mock_get.call_count == 2


class TestComponentSourceCaching:
    @patch("requests.get")
    def test_cached_source_served_on_checksum_match(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        client = RegistryClient(version="main")

        comp_dir = home_dir / ".starui" / "cache" / "registry" / "main" / "components"
        comp_dir.mkdir(parents=True)
        (comp_dir / "button.py").write_bytes(BUTTON_SOURCE.encode("utf-8"))

        source = client.get_component_source("button")
        assert source == BUTTON_SOURCE
        assert mock_get.call_count == 1

    @patch("requests.get")
    def test_stale_cache_refetches_source(self, mock_get, home_dir):
        mock_get.side_effect = [
            _make_response(TEST_INDEX_TEXT),
            _make_response(BUTTON_SOURCE),
        ]

        client = RegistryClient(version="main")

        comp_dir = home_dir / ".starui" / "cache" / "registry" / "main" / "components"
        comp_dir.mkdir(parents=True)
        (comp_dir / "button.py").write_text("# outdated content")

        source = client.get_component_source("button")
        assert source == BUTTON_SOURCE
        assert mock_get.call_count == 2

    @patch("requests.get")
    def test_source_network_error_falls_back_to_stale_cache(self, mock_get, home_dir):
        stale_source = "# stale but usable\ndef Button(): pass\n"
        call_count = [0]

        def side_effect_fn(*_args, **_kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_response(TEST_INDEX_TEXT)
            raise requests.ConnectionError("offline")

        mock_get.side_effect = side_effect_fn

        client = RegistryClient(version="main")

        comp_dir = home_dir / ".starui" / "cache" / "registry" / "main" / "components"
        comp_dir.mkdir(parents=True)
        (comp_dir / "button.py").write_text(stale_source)

        source = client.get_component_source("button")
        assert source == stale_source

    @patch("requests.get")
    def test_source_network_error_no_cache_raises(self, mock_get, home_dir):
        call_count = [0]

        def side_effect_fn(*_args, **_kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_response(TEST_INDEX_TEXT)
            raise requests.ConnectionError("offline")

        mock_get.side_effect = side_effect_fn

        client = RegistryClient(version="main")
        with pytest.raises(ConnectionError, match="Cannot fetch component"):
            client.get_component_source("button")


class TestCorruptedCache:
    @patch("requests.get")
    def test_corrupted_index_cache_refetches(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        cache_dir = home_dir / ".starui" / "cache" / "registry" / "main"
        cache_dir.mkdir(parents=True)
        (cache_dir / "index.json").write_text("not valid json{{{")
        (cache_dir / "index.meta.json").write_text(json.dumps({"fetched_at": time.time()}))

        client = RegistryClient(version="main")
        components = client.list_components()
        assert "button" in components
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_corrupted_index_cache_plus_network_failure(self, mock_get, home_dir):
        mock_get.side_effect = requests.ConnectionError("offline")

        cache_dir = home_dir / ".starui" / "cache" / "registry" / "main"
        cache_dir.mkdir(parents=True)
        (cache_dir / "index.json").write_text("not valid json{{{")
        (cache_dir / "index.meta.json").write_text(json.dumps({"fetched_at": time.time()}))

        client = RegistryClient(version="main")
        with pytest.raises(ConnectionError, match="Cannot fetch component registry"):
            client.list_components()

    @patch("requests.get")
    def test_corrupted_meta_invalidates_cache(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        cache_dir = home_dir / ".starui" / "cache" / "registry" / "main"
        cache_dir.mkdir(parents=True)
        (cache_dir / "index.json").write_text(TEST_INDEX_TEXT)
        (cache_dir / "index.meta.json").write_text("not json")

        client = RegistryClient(version="main")
        client.list_components()
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_missing_meta_invalidates_non_immutable_cache(self, mock_get, home_dir):
        mock_get.return_value = _make_response(TEST_INDEX_TEXT)

        cache_dir = home_dir / ".starui" / "cache" / "registry" / "main"
        cache_dir.mkdir(parents=True)
        (cache_dir / "index.json").write_text(TEST_INDEX_TEXT)

        client = RegistryClient(version="main")
        client.list_components()
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_missing_meta_okay_for_immutable(self, mock_get, home_dir):
        cache_dir = home_dir / ".starui" / "cache" / "registry" / "v1.0.0"
        cache_dir.mkdir(parents=True)
        (cache_dir / "index.json").write_text(TEST_INDEX_TEXT)

        client = RegistryClient(version="v1.0.0")
        components = client.list_components()
        assert "button" in components
        mock_get.assert_not_called()


class TestNoNetworkAvailable:
    @patch("requests.get")
    def test_no_cache_no_network_raises(self, mock_get, home_dir):
        mock_get.side_effect = requests.ConnectionError("offline")

        client = RegistryClient(version="main")
        with pytest.raises(ConnectionError, match="Check your network connection"):
            client.list_components()

    @patch("requests.get")
    def test_constructor_creates_cache_directory(self, mock_get, home_dir):
        RegistryClient(version="v2.0.0")
        expected = home_dir / ".starui" / "cache" / "registry" / "v2.0.0"
        assert expected.is_dir()
