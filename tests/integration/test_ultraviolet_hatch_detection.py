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
from gameboy_automation.games.pokemon.ultraviolet.screens.day_care_screen import (
    DayCareScreen,
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
) -> PartySlot | None:
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

    print("No Egg found in party.")

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

    return None

def pick_up_next_egg(
    emulator: MGBAEmulator,
) -> None:
    """Talk to the Day Care Man and accept the available Egg."""
    print()
    print("Picking up next Egg...")

    print("Starting Day Care Man conversation...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    # Ah, it's you!
    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    # We were raising your POKEMON...
    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    # Your POKEMON had an EGG!
    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    # We don't know how it got there...
    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    # The YES/NO menu is delayed, just like the nickname menu.
    print("Waiting for Egg YES/NO menu...")
    time.sleep(5.0)

    print("Accepting Egg...")

    # YES is already selected.
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    # Luke received the EGG...
    print("Advancing received-Egg dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    # Take good care of it.
    print("Finishing Day Care Man conversation...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(2.0)

    print("Closing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    print("Next Egg picked up!")

def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        load_game(
            emulator,
        )

        print()
        print("Checking for startup quick save...")

        if emulator.quick_save_exists():
            print("Quick save already exists.")
        else:
            print("No quick save exists. Creating one...")

            emulator.quick_save()

            time.sleep(1.0)

            if not emulator.quick_save_exists():
                raise RuntimeError(
                    "Startup quick save was not created."
                )

            print("Startup quick save created successfully.")

        egg_slot = find_egg_slot(
            emulator,
        )

        if egg_slot is None:
            print()
            print("No Egg in party. Picking up next Egg...")

            day_care_screen = DayCareScreen(
                session=emulator,
            )

            day_care_screen.move_to_day_care_approach()

            day_care_screen.move_to_day_care_man()

            pick_up_next_egg(
                emulator,
            )

            day_care_screen.move_to_hatching_route()

            egg_slot = find_egg_slot(
                emulator,
            )

            if egg_slot is None:
                raise RuntimeError(
                    "No Egg found after picking up an Egg "
                    "from the Day Care Man."
                )

            print()
            print("Creating pre-hatch quick save with newly acquired Egg...")

            emulator.quick_save()

            time.sleep(1.0)

            if not emulator.quick_save_exists():
                raise RuntimeError(
                    "Pre-hatch quick save was not created."
                )

            print("Pre-hatch quick save created successfully.")

        else:
            print()
            print(
                f"Egg already in party: {egg_slot.name}. "
                "Skipping Day Care pickup."
            )

        hatch_screen = HatchScreen(
            session=emulator,
        )

        print(f"Remembering Egg location: {egg_slot.name}")

        print()
        print("Checking for pre-hatch quick save...")

        if emulator.quick_save_exists():
            print(
                "Pre-hatch quick save already exists. "
                "Keeping existing quick save."
            )
        else:
            print("No pre-hatch quick save exists.")
            print("Creating pre-hatch quick save...")

            emulator.quick_save()

            time.sleep(1.0)

            if not emulator.quick_save_exists():
                raise RuntimeError(
                    "Pre-hatch quick save was not created."
                )

            print("Pre-hatch quick save created successfully.")

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

        stats = pokemon.stats

        archive_name = (
            f"{pokemon.species}_"
            f"{pokemon.nature.value}_"
            f"{stats.max_hp}_"
            f"{stats.attack}_"
            f"{stats.defense}_"
            f"{stats.special_attack}_"
            f"{stats.special_defense}_"
            f"{stats.speed}"
        )

        print(
            f"Archiving pre-hatch quick save as "
            f"{archive_name}.quick_save..."
        )

        archive_path = emulator.archive_quick_save(
            archive_name,
        )

        if archive_path is None:
            print(
                "No previous pre-hatch quick save exists. "
                "Nothing to archive."
            )
        else:
            print(
                f"Archived pre-hatch quick save: "
                f"{archive_path}"
            )
        print("Newly hatched Pokémon:")
        print(pokemon)



        time.sleep(3)

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

    finally:
        emulator.close()


if __name__ == "__main__":
    main()