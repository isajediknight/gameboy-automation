from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.games.pokemon.ultraviolet.screens.title_screen import (  # noqa: E402
    TitleScreen,
)


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

        time.sleep(3)

        for _ in range(3):
            print("Pressing START to skip startup")

            emulator.press(
                Button.START,
                duration_seconds=0.2,
            )

            time.sleep(1)

        print("Waiting for title screen to settle...")
        time.sleep(5)

        #
        # TitleScreen currently expects a Session-like object with
        # screenshot(). MGBAEmulator already provides that interface.
        #

        title_screen = TitleScreen(
            session=emulator,
        )

        screen = emulator.screenshot()

        diagnostic_path = (
            repo_root
            / "output"
            / "screenshots"
            / "ultraviolet_title_screen_live.png"
        )

        screen.save(diagnostic_path)

        print(f"Saved live title screen screenshot: {diagnostic_path}")

        print("Waiting for Ultra Violet title screen...")

        title_screen.wait_until_visible(
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
        )

        print("Ultra Violet title screen detected!")

        print("Pressing START through TitleScreen...")
        title_screen.press_start()

        time.sleep(3)

        print("START pressed successfully.")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()