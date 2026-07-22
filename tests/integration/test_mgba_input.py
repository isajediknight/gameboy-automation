from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402


def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        emulator.launch(
            ProjectPaths.ULTRAVIOLET_ROM,
        )

        print(f"Started mGBA ({emulator.pid})")

        emulator.wait_for_window()

        #
        # Allow the ROM startup screen to appear.
        #

        time.sleep(3)

        print("Pressing START")

        emulator.press(
            Button.START,
            duration_seconds=0.2,
        )

        time.sleep(1)

        print("Pressing START")

        emulator.press(
            Button.START,
            duration_seconds=0.2,
        )

        #
        # Keep the emulator open so the result can be observed.
        #

        print("Pressing START")

        emulator.press(
            Button.START,
            duration_seconds=0.2,
        )

        time.sleep(2)

        print("Pressing A")

        emulator.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(2)

        print("Holding RIGHT")

        emulator.hold(
            Button.RIGHT,
            duration_seconds=1.0,
        )

        time.sleep(5)

    finally:
        emulator.close()


if __name__ == "__main__":
    main()