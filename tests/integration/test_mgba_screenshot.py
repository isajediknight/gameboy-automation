from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.utils.windows import (  # noqa: E402
    capture_window,
    find_window_by_process_id,
)


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

        window_handle = None

        for _ in range(20):

            window_handle = find_window_by_process_id(
                emulator.pid,
            )

            if window_handle is not None:
                break

            time.sleep(0.5)

        if window_handle is None:
            raise RuntimeError(
                "Could not locate mGBA window."
            )

        #
        # Give Pokémon a couple seconds to finish loading.
        #

        time.sleep(2)

        image = capture_window(window_handle)

        output_file = (
            ProjectPaths.SCREENSHOTS
            / "ultraviolet_startup.png"
        )

        image.save(output_file)

        print()
        print(f"Screenshot saved to:")
        print(output_file)

        #
        # Keep emulator open briefly so you can compare.
        #

        time.sleep(3)

    finally:

        emulator.close()


if __name__ == "__main__":
    main()
