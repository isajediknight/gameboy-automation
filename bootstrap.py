from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
VENDOR = SRC / "gameboy_automation" / "_vendor"

for path in (SRC, VENDOR):
    path_string = str(path)

    if path_string not in sys.path:
        sys.path.insert(0, path_string)