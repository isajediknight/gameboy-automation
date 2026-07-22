from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402


def main() -> None:

    ProjectPaths.SCREENSHOTS.mkdir(
        parents=True,
        exist_ok=True,
    )

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
        # Give Pokémon a couple seconds to finish loading.
        #

        time.sleep(2)

        image = emulator.screenshot()

        output_file = (
            ProjectPaths.SCREENSHOTS
            / "ultraviolet_startup.png"
        )

        image.save(output_file)

        print()
        print("Screenshot saved to:")
        print(output_file)

        #
        # Keep emulator open briefly so you can compare.
        #

        time.sleep(3)

    finally:

        emulator.close()


if __name__ == "__main__":
    main()