from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.games.pokemon.ultraviolet.game import (  # noqa: E402
    UltraVioletGame,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (  # noqa: E402
    PauseMenu,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PartySlot,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen import (
    PokemonSummaryScreen,
)


EEVEE_SLOTS = (
    PartySlot.SLOT_1,
    PartySlot.SLOT_2,
    PartySlot.SLOT_3,
    PartySlot.SLOT_4,
    PartySlot.SLOT_5,
    PartySlot.SLOT_6,
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


def open_summary(
    emulator: MGBAEmulator,
    slot: PartySlot,
) -> PokemonSummaryScreen:
    pause_menu = PauseMenu(
        session=emulator,
    )

    print("Opening pause menu...")
    pause_menu.open()

    print("Opening Pokémon party screen...")
    party_screen = pause_menu.open_party()

    print(f"Selecting {slot.name}...")
    party_screen.select(
        slot,
    )

    print("Opening selected Pokémon action menu...")
    pokemon_menu = party_screen.open_selected()

    print("Opening Pokémon Summary...")
    pokemon_menu.confirm()

    summary_screen = PokemonSummaryScreen(
        session=emulator,
    )

    summary_screen.wait_until_info_visible(
        timeout_seconds=10.0,
        poll_interval_seconds=0.1,
    )

    return summary_screen


def test_eevee_slot(
    slot: PartySlot,
) -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        load_game(
            emulator,
        )

        summary_screen = open_summary(
            emulator,
            slot,
        )

        print(f"Reading Eevee summary from {slot.name}...")

        pokemon = summary_screen.read_summary()

        print(
            f"{slot.name}: {pokemon}"
        )

        assert pokemon.species == "EEVEE"
        assert pokemon.level == 5

        print(
            f"{slot.name} Eevee detected successfully!"
        )

    finally:
        emulator.close()


def main() -> None:
    for slot in EEVEE_SLOTS:
        print()
        print("=" * 80)
        print(f"Testing {slot.name}")
        print("=" * 80)

        test_eevee_slot(
            slot,
        )

    print()
    print("All Level 6 Eevee slots detected successfully!")


if __name__ == "__main__":
    main()
