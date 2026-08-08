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
    PokemonSummaryPage,
    PokemonSummaryScreen,
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

        print("Navigating to Pokémon Skills page...")

        summary_screen.go_to(
            PokemonSummaryPage.SKILLS,
        )

        print("Reading Pokémon current HP...")

        current_hp = summary_screen.current_hp()

        print(f"Detected current HP: {current_hp}")

        assert current_hp == 233

        print("Pokémon current HP detected successfully!")

        print("Capturing maximum HP region...")

        summary_screen.max_hp()

        max_hp = summary_screen.max_hp()

        print(f"Detected maximum HP: {max_hp}")

        assert max_hp == 233

        print("Capturing Attack region...")

        summary_screen.attack()

        print("Reading Pokémon Attack...")

        attack = summary_screen.attack()

        print(f"Detected Attack: {attack}")

        assert attack == 127

        print("Pokémon Attack detected successfully!")

        print("Capturing Defense region...")

        summary_screen.defense()

        print("Reading Pokémon Defense...")

        defense = summary_screen.defense()

        print(f"Detected Defense: {defense}")

        assert defense == 101

        print("Pokémon Defense detected successfully!")

        print("Capturing Special Attack region...")

        summary_screen.special_attack()

        print("Reading Pokémon Special Attack...")

        special_attack = summary_screen.special_attack()

        print(f"Detected Special Attack: {special_attack}")

        assert special_attack == 129

        print("Pokémon Special Attack detected successfully!")

        print("Capturing Special Defense region...")

        summary_screen.special_defense()

        print("Reading Pokémon Special Defense...")

        special_defense = summary_screen.special_defense()

        print(f"Detected Special Defense: {special_defense}")

        assert special_defense == 132

        print("Pokémon Special Defense detected successfully!")

        print("Capturing Speed region...")

        summary_screen.speed()

        print("Reading Pokémon Speed...")

        speed = summary_screen.speed()

        print(f"Detected Speed: {speed}")

        assert speed == 127

        print("Pokémon Speed detected successfully!")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()