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
from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import PauseMenu
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PartyScreen,
    PartySlot,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen import (
    PokemonSummaryScreen,
)

def load_game(emulator: MGBAEmulator) -> UltraVioletGame:
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

    return game

def open_party(emulator: MGBAEmulator) -> PartyScreen:
    pause_menu = PauseMenu(session=emulator)

    print("Opening pause menu...")
    pause_menu.open()

    print("Opening Pokémon party screen...")
    return pause_menu.open_party()


def open_summary(
    emulator: MGBAEmulator,
    party_screen: PartyScreen,
    slot: PartySlot,
) -> PokemonSummaryScreen:
    print(f"Selecting {slot.name}...")
    party_screen.select(slot)

    print("Opening selected Pokémon action menu...")
    pokemon_menu = party_screen.open_selected()

    print("Opening Pokémon Summary...")
    pokemon_menu.confirm()

    summary_screen = PokemonSummaryScreen(session=emulator)
    summary_screen.wait_until_info_visible(
        timeout_seconds=10.0,
        poll_interval_seconds=0.1,
    )

    return summary_screen

def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        load_game(emulator)

        party_screen = open_party(emulator)

        print("Checking SLOT_1 for Egg...")

        assert party_screen.is_egg(
            PartySlot.SLOT_1,
        ) is False

        print("SLOT_1 correctly detected as Pokémon.")

        print("Checking SLOT_2 for Egg...")

        assert party_screen.is_egg(
            PartySlot.SLOT_2,
        ) is True

        print("SLOT_2 correctly detected as Egg.")

        print("Egg party detection successful!")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()