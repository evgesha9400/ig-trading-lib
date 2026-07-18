# tests/conftest.py  (root)
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()  # reads .env if present
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SRC = PROJECT_ROOT / "src"
# If PYTHONPATH=src isn’t already active, ensure src is added:
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
