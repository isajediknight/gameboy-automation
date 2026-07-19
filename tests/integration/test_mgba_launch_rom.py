from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402


def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    emulator.launch(
        rom_path=ProjectPaths.ULTRAVIOLET_ROM,
    )

    print(f"Started mGBA with process ID: {emulator.pid}")
    print(f"Loaded ROM: {emulator.rom_path}")

    time.sleep(8)

    emulator.close()

    print("mGBA and ROM closed successfully.")


if __name__ == "__main__":
    main()