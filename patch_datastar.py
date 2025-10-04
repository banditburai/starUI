"""Monkey-patch starhtml.datastar with local development version."""
import sys
import importlib.util
from pathlib import Path

# Find datastar.py relative to this patch file
patch_dir = Path(__file__).parent
datastar_path = patch_dir / "datastar.py"

# Load local datastar.py as a module
spec = importlib.util.spec_from_file_location("datastar_local", str(datastar_path))
datastar_local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(datastar_local)

# Replace starhtml.datastar with our local version
sys.modules['starhtml.datastar'] = datastar_local

# Also make it available as just 'datastar' for direct imports
sys.modules['datastar'] = datastar_local

print(f"[PATCH] Replaced starhtml.datastar with {datastar_path}")
