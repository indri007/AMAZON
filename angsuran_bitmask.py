"""angsuran_bitmask.py - Re-export for backward compatibility."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src" / "assembly"))
from angsuran_bitmask import *

if __name__ == "__main__":
    main()
