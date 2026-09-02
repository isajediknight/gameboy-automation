from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.games.pokemon.ultraviolet.game import UltraVioletGame
from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_center_screen import (
    PokemonCenterScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.day_care_screen import (
    DayCareScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pc_screen import (
    PCScreen,
)

POKEMON_CENTER_TEMPLATE_DIRECTORY = (
    repo_root
    / "src"
    / "gameboy_automation"
    / "games"
    / "pokemon"
    / "ultraviolet"
    / "assets"
    / "templates"
    / "screens"
    / "pokemon_center"
)

PC_TEMPLATE_PATH = (
    POKEMON_CENTER_TEMPLATE_DIRECTORY
    / "pc.png"
)

PLAYER_UP_TEMPLATE_PATH = (
    repo_root
    / "src"
    / "gameboy_automation"
    / "games"
    / "pokemon"
    / "ultraviolet"
    / "assets"
    / "templates"
    / "screens"
    / "day_care"
    / "player"
    / "on_foot"
    / "full"
    / "up.png"
)


def load_game(
    emulator: MGBAEmulator,
) -> UltraVioletGame:
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

    print("Loading saved game...")

    game = UltraVioletGame(
        session=emulator,
    )

    game.load_saved_game()

    print("Saved game loaded!")

    return game


def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        load_game(
            emulator,
        )

        day_care = DayCareScreen(
            session=emulator,
        )

        pokemon_center = PokemonCenterScreen(
            session=emulator,
        )

        print()
        print("Moving from Day Care route to Pokémon Center...")

        day_care.move_to_pokemon_center()

        time.sleep(3)

        print()
        print("Moving from Pokémon Center entrance to PC...")

        pokemon_center.move_to_pc()

        print()
        print("Reached Pokémon Center PC successfully!")

        print()
        print("Opening PC deposit interface...")

        pc_screen = PCScreen(
            session=emulator,
        )

        pc_screen.open_deposit_party()

        print()
        print("Depositing SLOT_6 through SLOT_2...")

        pc_screen.deposit_all_except_first()

        print()
        print(
            "Full-party Pokémon Center deposit workflow "
            "completed successfully!"
        )

    finally:
        emulator.close()


if __name__ == "__main__":
    main()