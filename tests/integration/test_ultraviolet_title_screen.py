from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.games.pokemon.ultraviolet.game import (  # noqa: E402
    UltraVioletGame,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (  # noqa: E402
    PauseMenu,
    PauseMenuSelection,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (  # noqa: E402
    PartyScreen,
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

        game.load_saved_game()

        print("Saved game loaded!")

        pause_menu = PauseMenu(
            session=emulator,
        )

        print("Opening pause menu...")

        pause_menu.open()

        print("Pause menu opened!")

        current_selection = pause_menu.selected_item()

        print(f"Current pause menu selection: {current_selection.name}")

        print("Selecting POKEMON...")

        print("Opening Pokémon party screen...")

        party_screen = pause_menu.open_party()

        print("Party screen detected!")

        try:
            selected_slot = party_screen.selected_slot()

            print(f"Selected party slot: {selected_slot.name}")

        except Exception as exc:
            print(f"selected_slot() failed: {exc}")

            print("Leaving emulator open for inspection...")

            time.sleep(10)

            raise

        emulator.press(
            Button.DOWN,
        )

        time.sleep(2)


        try:
            selected_slot = party_screen.selected_slot()

            print(f"Selected party slot after DOWN: {selected_slot.name}")

        except Exception as exc:
            print(f"selected_slot() after DOWN failed: {exc}")

            print("Leaving emulator open for inspection...")

            time.sleep(10)

            raise


        time.sleep(2)

    finally:
        emulator.close()


if __name__ == "__main__":
    main()