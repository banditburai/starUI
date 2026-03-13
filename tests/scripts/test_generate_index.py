"""Tests for scripts/generate_index.py extract_dependencies()."""

import sys
from pathlib import Path

# Add scripts dir to path so we can import generate_index
SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from generate_index import extract_dependencies  # noqa: E402


class TestExtractDependencies:
    def test_relative_imports(self, tmp_path):
        f = tmp_path / "comp.py"
        f.write_text("from .utils import cn\nfrom .button import Button\n")
        assert extract_dependencies(f) == ["button", "utils"]

    def test_absolute_component_imports(self, tmp_path):
        f = tmp_path / "block.py"
        f.write_text("from components.avatar import Avatar\nfrom components.utils import cn\n")
        assert extract_dependencies(f) == ["avatar", "utils"]

    def test_mixed_imports(self, tmp_path):
        f = tmp_path / "mixed.py"
        f.write_text("from .utils import cn\nfrom components.avatar import Avatar\n")
        assert extract_dependencies(f) == ["avatar", "utils"]

    def test_non_component_imports_ignored(self, tmp_path):
        f = tmp_path / "comp.py"
        f.write_text("from starhtml import FT\nimport os\nfrom pathlib import Path\n")
        assert extract_dependencies(f) == []

    def test_no_imports(self, tmp_path):
        f = tmp_path / "comp.py"
        f.write_text("def Button(): pass\n")
        assert extract_dependencies(f) == []

    def test_deduplicates(self, tmp_path):
        f = tmp_path / "comp.py"
        f.write_text("from .utils import cn\nfrom .utils import cva\n")
        assert extract_dependencies(f) == ["utils"]

    def test_plain_components_import_ignored(self, tmp_path):
        """'from components import something' (no dot) is not a dep."""
        f = tmp_path / "comp.py"
        f.write_text("from components import something\n")
        assert extract_dependencies(f) == []

    def test_multiline_import(self, tmp_path):
        f = tmp_path / "comp.py"
        f.write_text("from components.dropdown_menu import (\n    DropdownMenu,\n    DropdownMenuContent,\n)\n")
        assert extract_dependencies(f) == ["dropdown_menu"]
