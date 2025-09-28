"""Test configuration for pytest."""
import sys
from pathlib import Path

# Ensure both the project root and src directory are importable for tests.
ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"

for path in (ROOT, SRC_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
