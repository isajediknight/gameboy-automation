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
from gameboy_automation.games.pokemon.ultraviolet.screens.day_care_screen import (
    DayCareScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_center_screen import (
    PokemonCenterScreen,
)

MOVE_SECONDS = 0.1


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

    egg_slot = party_screen.find_egg_slot()

    party_screen.exit_to_overworld()

    return egg_slot

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

            emulator.create_quick_save()

            print("Startup quick save created successfully.")

        egg_slot = find_egg_slot(
            emulator,
        )

        if egg_slot is None:
            print()
            print("No Egg in party.")

            day_care_screen = DayCareScreen(
                session=emulator,
            )

            print()
            print("Checking party size...")

            pause_menu = PauseMenu(
                session=emulator,
            )

            pause_menu.open()

            party_screen = pause_menu.open_party()

            party_size = party_screen.party_size()

            print(f"Party contains {party_size} occupied slots.")

            party_screen.exit_to_overworld()

            if party_size == 6:
                print()
                print(
                    "Party is full. Depositing Pokémon "
                    "before picking up Egg..."
                )

                pokemon_center_screen = PokemonCenterScreen(
                    session=emulator,
                )

                day_care_screen.move_to_pokemon_center()

                # Allow the Pokémon Center map transition to settle.
                time.sleep(3.0)

                pokemon_center_screen.deposit_all_except_first()

                # Allow the exterior map transition to settle.
                time.sleep(3.0)

                day_care_screen.move_from_pokemon_center()

                print()
                print(
                    "Returned to Day Care after clearing "
                    "party space."
                )

            day_care_screen.pick_up_egg_and_return_to_hatching_route()

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

            emulator.create_quick_save()

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

            emulator.create_quick_save()

            print("Pre-hatch quick save created successfully.")

        print()
        print("Turning fast-forward ON...")
        emulator.toggle_fast_forward()

        hatch_screen.wait_for_hatch(
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

        print(
            f"Opening newly hatched Pokémon summary "
            f"in {hatched_slot.name}..."
        )

        summary_screen = party_screen.open_summary(
            hatched_slot,
        )

        print("Reading newly hatched Pokémon summary...")

        pokemon = summary_screen.read_summary()

        archive_name = pokemon.archive_name

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
        print("Returning to pause menu...")

        pause_menu.return_to_menu()

        print("Saving game...")

        pause_menu.save_game()

    finally:
        emulator.close()


if __name__ == "__main__":
    main()