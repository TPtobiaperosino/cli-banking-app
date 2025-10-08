"""Pytest configuration.

Prefer installing the project in editable mode instead of mutating ``sys.path``:

    pip install -e .

This file only ensures ``src`` is importable when tests are run without an
editable install (e.g., in a quick local clone). In CI you should install the
package so this file becomes unnecessary.
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if SRC.is_dir():
    src_str = str(SRC)
    if src_str not in sys.path:
        # Insert after the script directory (index 1) to avoid shadowing stdlib.
        sys.path.insert(1, src_str)
