from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators import Button  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.games.pokemon.ultraviolet.screens.title_screen import (  # noqa: E402
    TitleScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.load_menu import (  # noqa: E402
    LoadMenu,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.quest_recap import (  # noqa: E402
    QuestRecap,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (  # noqa: E402
    PauseMenu,
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

        #
        # TitleScreen currently expects a Session-like object with
        # screenshot(). MGBAEmulator already provides that interface.
        #

        title_screen = TitleScreen(
            session=emulator,
        )

        screen = emulator.screenshot()

        diagnostic_path = (
            repo_root
            / "output"
            / "screenshots"
            / "ultraviolet_title_screen_live.png"
        )

        screen.save(diagnostic_path)

        print(f"Saved live title screen screenshot: {diagnostic_path}")

        print("Waiting for Ultra Violet title screen...")

        title_screen.wait_until_visible(
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
        )

        print("Ultra Violet title screen detected!")

        print("Pressing START through TitleScreen...")
        title_screen.press_start()

        load_menu = LoadMenu(
            session=emulator,
        )

        print("Waiting for Ultra Violet load menu...")

        load_menu.wait_until_visible(
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
        )

        print("Ultra Violet load menu detected!")

        time.sleep(1)

        print("Continuing Luke's saved game...")

        before_continue = emulator.screenshot()

        before_continue.save(
            repo_root
            / "output"
            / "screenshots"
            / "before_continue_game.png"
        )

        load_menu.continue_game()

        quest_recap = QuestRecap(
            session=emulator,
        )

        time.sleep(2)

        load_menu.continue_game()

        time.sleep(1)

        after_continue = emulator.screenshot()

        after_continue.save(
            repo_root
            / "output"
            / "screenshots"
            / "after_continue_game.png"
        )

        print("Waiting for quest recap...")

        quest_recap.wait_until_visible(
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
        )

        time.sleep(1)

        print("Advancing quest recap...")
        quest_recap.advance()

        time.sleep(2)

        print("Advancing quest recap...")
        quest_recap.advance()

        time.sleep(2)

        print("Advancing quest recap...")
        quest_recap.advance()

        time.sleep(2)

        print("Advancing quest recap...")
        quest_recap.advance()

        time.sleep(2)

        print("Advancing quest recap...")
        quest_recap.advance()

        time.sleep(2)

        print("Pressing START from overworld...")

        emulator.press(
            Button.START,
        )

        pause_menu = PauseMenu(
            session=emulator,
        )

        print("Waiting for pause menu...")

        pause_menu.wait_until_visible(
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
        )

        print("Pause menu detected!")

        time.sleep(2)

    finally:
        emulator.close()


if __name__ == "__main__":
    main()