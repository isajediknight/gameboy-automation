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
from gameboy_automation.games.pokemon.ultraviolet.screens.hatch_screen import (
    HatchScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (
    PauseMenu,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PartySlot,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen import (
    PokemonSummaryScreen,
)

MOVE_SECONDS = 0.1
POLL_INTERVAL_SECONDS = 0.1


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


def move_until_hatch(
    emulator: MGBAEmulator,
    hatch_screen: HatchScreen,
    button: Button,
    duration_seconds: float,
) -> bool:
    print(
        f"Holding {button.name} for up to "
        f"{duration_seconds:.1f} seconds..."
    )

    emulator.key_down(
        button,
    )

    try:
        deadline = time.monotonic() + duration_seconds

        while time.monotonic() < deadline:
            if hatch_screen.is_visible():
                print("Hatch sequence detected!")
                return True

            time.sleep(
                POLL_INTERVAL_SECONDS,
            )

        return False

    finally:
        emulator.key_up(
            button,
        )

def find_egg_slot(
    emulator: MGBAEmulator,
) -> PartySlot:
    """Find and return the party slot containing the Egg."""
    print()
    print("Locating Egg in party...")

    pause_menu = PauseMenu(
        session=emulator,
    )

    pause_menu.open()

    party_screen = pause_menu.open_party()

    party_size = party_screen.party_size()

    print(f"Party contains {party_size} occupied slots.")

    for slot_number in range(1, party_size + 1):
        slot = PartySlot(
            slot_number,
        )

        print(f"Checking {slot.name}...")

        if party_screen.is_egg(
            slot,
        ):
            print(f"Egg found in {slot.name}!")

            # Leave the party screen and return to the overworld.
            emulator.press(
                Button.B,
                duration_seconds=0.2,
            )

            time.sleep(1)

            emulator.press(
                Button.B,
                duration_seconds=0.2,
            )

            return slot

    raise RuntimeError(
        "No Egg was found in the Pokémon party."
    )

def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        load_game(
            emulator,
        )

        hatch_screen = HatchScreen(
            session=emulator,
        )

        egg_slot = find_egg_slot(
            emulator,
        )

        print(f"Remembering Egg location: {egg_slot.name}")

        print()
        print("Turning fast-forward ON...")
        emulator.toggle_fast_forward()

        hatch_detected = False

        while not hatch_detected:
            hatch_detected = move_until_hatch(
                emulator,
                hatch_screen,
                Button.RIGHT,
                MOVE_SECONDS,
            )

            if hatch_detected:
                break

            hatch_detected = move_until_hatch(
                emulator,
                hatch_screen,
                Button.LEFT,
                MOVE_SECONDS,
            )

        print("Turning fast-forward OFF...")
        emulator.toggle_fast_forward()

        print()
        print("Hatch detection test completed successfully!")

        print()
        print("Finishing hatch sequence...")

        hatch_screen.finish_hatch()

        time.sleep(2)

        print("Hatch sequence completed!")

        print()
        print("Waiting for overworld controls to return...")
        time.sleep(2.0)

        print("Opening pause menu...")

        pause_menu = PauseMenu(
            session=emulator,
        )

        pause_menu.open()

        print("Pause menu opened.")

        print("Opening Pokémon party...")

        party_screen = pause_menu.open_party()

        print("Pokémon party opened successfully!")

        hatched_slot = egg_slot

        print(f"Selecting newly hatched Pokémon in {hatched_slot.name}...")

        party_screen.select(
            hatched_slot,
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

        print("Reading newly hatched Pokémon summary...")

        pokemon = summary_screen.read_summary()

        print()
        print("Newly hatched Pokémon:")
        print(pokemon)

        print()
        print("Saving game...")

        # Return from Pokémon Summary to the pause menu.
        for press_number in range(1, 6):
            print(f"Pressing B #{press_number}...")

            emulator.press(
                Button.B,
                duration_seconds=0.2,
            )

            time.sleep(1.0)

            pause_menu_visible = pause_menu.is_visible()

            print(
                f"After B #{press_number}: "
                f"pause_menu={pause_menu_visible}"
            )

            if pause_menu_visible:
                print("Returned to pause menu.")
                break

        else:
            raise RuntimeError(
                "Could not return to pause menu "
                "after 5 B presses."
            )

        print("Saving game...")

        pause_menu.save_game()

        print("Creating quick save...")

        time.sleep(10)

        emulator.quick_save()

        print("Quick save completed!")

        time.sleep(2)

    finally:
        emulator.close()


if __name__ == "__main__":
    main()