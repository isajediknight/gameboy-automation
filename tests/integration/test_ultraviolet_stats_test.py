from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.emulators import Button
from gameboy_automation.config import ProjectPaths  # noqa: E402
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
    PokemonNature,
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

        print("Opening Pokémon party screen...")

        party_screen = pause_menu.open_party()

        print("Selecting SLOT_3...")

        party_screen.select(
            PartySlot.SLOT_3,
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

        print("Capturing Pokémon species region...")

        summary_screen.species()

        print("Reading complete Pokémon summary...")

        pokemon = summary_screen.read_summary()

        print(pokemon)

        assert pokemon.level == 25
        assert pokemon.nature is PokemonNature.TIMID

        assert pokemon.stats.current_hp == 68
        assert pokemon.stats.max_hp == 68
        assert pokemon.stats.attack == 33
        assert pokemon.stats.defense == 41
        assert pokemon.stats.special_attack == 48
        assert pokemon.stats.special_defense == 47
        assert pokemon.stats.speed == 31
        assert pokemon.stats.experience == 15625
        assert pokemon.stats.next_level_experience == 1951

        print("Complete Pokémon summary detected successfully!")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()