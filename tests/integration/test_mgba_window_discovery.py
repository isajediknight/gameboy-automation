from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.utils.windows import (  # noqa: E402
    find_window_by_process_id,
    get_window_title,
)


def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        emulator.launch(
            rom_path=ProjectPaths.ULTRAVIOLET_ROM,
        )

        print(f"Started mGBA with process ID: {emulator.pid}")

        window_handle: int | None = None

        for _ in range(20):
            if emulator.pid is None:
                break

            window_handle = find_window_by_process_id(
                emulator.pid,
            )

            if window_handle is not None:
                break

            time.sleep(0.5)

        if window_handle is None:
            raise RuntimeError(
                "Could not locate the visible mGBA window."
            )

        window_title = get_window_title(window_handle)

        print(f"Window handle: {window_handle}")
        print(f"Window title: {window_title}")
        print("mGBA window discovered successfully.")

        time.sleep(3)

    finally:
        emulator.close()


if __name__ == "__main__":
    main()