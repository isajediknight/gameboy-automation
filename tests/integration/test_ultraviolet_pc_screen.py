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
from gameboy_automation.games.pokemon.ultraviolet.screens.pc_screen import (
    PCScreen,
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

        print()
        print("Testing PC Deposit Pokémon navigation...")

        pc_screen = PCScreen(
            session=emulator,
        )

        pc_screen.open_deposit_party()
        print()
        print("Testing full-party deposit...")

        pc_screen.deposit_all_except_first()

        print()
        print(
            "Full-party deposit completed successfully!"
        )
        

    finally:
        emulator.close()


if __name__ == "__main__":
    main()