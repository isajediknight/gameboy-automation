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


def hold_button(
    emulator: MGBAEmulator,
    button: Button,
    duration_seconds: float,
) -> None:
    print(
        f"Holding {button.name} for "
        f"{duration_seconds:.1f} seconds..."
    )

    emulator.key_down(
        button,
    )

    try:
        time.sleep(
            duration_seconds,
        )

    finally:
        emulator.key_up(
            button,
        )

    print(
        f"Released {button.name}."
    )


def main() -> None:
    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        load_game(
            emulator,
        )

        print()
        print("Starting fast-forward movement test...")

        print("Turning fast-forward ON...")
        emulator.toggle_fast_forward()

        hold_button(
            emulator,
            Button.RIGHT,
            3.0,
        )

        time.sleep(1.0)

        hold_button(
            emulator,
            Button.LEFT,
            3.0,
        )

        print("Turning fast-forward OFF...")
        emulator.toggle_fast_forward()

        print()
        print("Fast-forward movement test completed successfully!")

    finally:
        emulator.close()


if __name__ == "__main__":
    main()