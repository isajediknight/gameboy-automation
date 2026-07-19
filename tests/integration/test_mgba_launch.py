from pathlib import Path
import sys
import time

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.emulators.mgba import MGBAEmulator


def main() -> None:

    emulator = MGBAEmulator(
        executable_path=(
            repo_root
            / "emulators"
            / "mgba"
            / "executable"
            / "mGBA.exe"
        )
    )

    emulator.launch()

    print(f"Started mGBA with process ID: {emulator.pid}")

    time.sleep(5)

    emulator.close()

    print("mGBA closed successfully.")


if __name__ == "__main__":
    main()