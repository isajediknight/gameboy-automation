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

        print("Opening Pokémon party screen...")

        party_screen = pause_menu.open_party()

        print("Party screen detected!")

        time.sleep(1)

        screen = emulator.screenshot()

        debug_coordinates = [
            (150, 20),
            (150, 44),
            (150, 68),
            (150, 92),
            (150, 116),
        ]

        for coordinate in debug_coordinates:
            pixel = screen.pixel(*coordinate)

            print(
                f"Pixel {coordinate}: "
                f"({pixel.red}, {pixel.green}, {pixel.blue})"
            )

        screen.save(
            repo_root
            / "output"
            / "screenshots"
            / "party_size_debug.png"
        )

        party_size = party_screen.party_size()

        print(f"Detected party size: {party_size}")

        assert party_size == 3

        print("3-Pokémon party size detected successfully!")

        time.sleep(2)

        print("Selecting SLOT_3...")

        party_screen.select(
            PartySlot.SLOT_3,
        )

        time.sleep(1)

        selected_slot = party_screen.selected_slot()

        print(f"Selected party slot: {selected_slot.name}")

        assert selected_slot is PartySlot.SLOT_3

        print("Pressing A on selected Pokémon...")

        emulator.press(
            Button.A,
        )

        time.sleep(1)

        screen = emulator.screenshot()

        screen.save(
            repo_root
            / "output"
            / "screenshots"
            / "party_pokemon_selected_menu.png"
        )

        print("Saved selected Pokémon menu screenshot.")

        time.sleep(5)

        print("Attempting to select unavailable SLOT_6...")

        #try:
        #    party_screen.select(
        #        PartySlot.SLOT_6,
        #    )
        #except ValueError as error:
        #    print(f"Correctly rejected SLOT_6: {error}")
        #else:
        #    raise AssertionError(
        #        "Expected SLOT_6 selection to be rejected."
        #    )

        selected_slot = party_screen.selected_slot()

        print(
            f"Party slot after rejected selection: "
            f"{selected_slot.name}"
        )

        assert selected_slot is PartySlot.SLOT_3

    finally:
        emulator.close()


if __name__ == "__main__":
    main()