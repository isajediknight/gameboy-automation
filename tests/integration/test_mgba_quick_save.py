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

        print("Loading saved game...")

        game = UltraVioletGame(
            session=emulator,
        )

        game.load_saved_game()

        print("Saved game loaded!")

        time.sleep(1)

        print("Creating quick save...")
        emulator.quick_save()

        time.sleep(1)

        print("Quick save command completed successfully!")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()