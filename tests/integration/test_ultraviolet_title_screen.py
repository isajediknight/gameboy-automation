from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (  # noqa: E402
    PauseMenu,
)
from gameboy_automation.games.pokemon.ultraviolet.game import (  # noqa: E402
    UltraVioletGame,
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
        time.sleep(2)

        print("Loading saved game through UltraVioletGame...")

        game = UltraVioletGame(
            session=emulator,
        )

        quest_recap = game.load_saved_game()

        print("Saved game loaded to quest recap!")

        for _ in range(5):
            print("Advancing quest recap...")

            quest_recap.advance()

            time.sleep(2)

        print("Pressing START from overworld...")

        emulator.press(
            Button.START,
        )

        pause_menu = PauseMenu(
            session=emulator,
        )

        print("Waiting for pause menu...")

        pause_menu.wait_until_visible(
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
        )

        print("Pause menu detected!")

        time.sleep(2)

    finally:
        emulator.close()


if __name__ == "__main__":
    main()
