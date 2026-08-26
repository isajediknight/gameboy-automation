from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button
from gameboy_automation.emulators.mgba import MGBAEmulator
from gameboy_automation.games.pokemon.ultraviolet.game import UltraVioletGame
from gameboy_automation.games.pokemon.ultraviolet.screens.day_care_screen import (
    DayCareScreen,
)

ROUTE_MAP_PATH = (
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
    / "route_map.png"
)

def load_game(emulator: MGBAEmulator) -> None:
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

    game = UltraVioletGame(
        session=emulator,
    )

    print("Loading saved game...")
    game.load_saved_game()

    print("Saved game loaded!")

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

    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    print("Advancing dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    print("Waiting for Egg YES/NO menu...")
    time.sleep(5.0)

    print("Accepting Egg...")

    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

    print("Advancing received-Egg dialogue...")
    emulator.press(
        Button.A,
        duration_seconds=0.2,
    )

    time.sleep(1.0)

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

        day_care_screen = DayCareScreen(
            session=emulator,
        )

        print()
        print("Testing movement to Day Care approach point...")

        day_care_screen.move_to_day_care_approach()

        position = day_care_screen.player_map_position()

        print(
            f"Final player map position: "
            f"x={position.x}, "
            f"y={position.y}"
        )

        print("Day Care approach movement completed successfully!")

        print()
        print("Testing final movement to Day Care Man...")

        day_care_screen.move_to_day_care_man()

        print("Day Care Man reached successfully!")

        pick_up_next_egg(
            emulator,
        )

        print()
        print("Testing return to hatching route...")

        day_care_screen.move_to_hatching_route()

        position = day_care_screen.player_map_position()

        print(
            f"Final hatching route position: "
            f"x={position.x}, "
            f"y={position.y}"
        )

        print("Returned to hatching route successfully!")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()