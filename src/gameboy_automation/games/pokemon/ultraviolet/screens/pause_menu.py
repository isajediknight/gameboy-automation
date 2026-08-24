from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button
from enum import Enum
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PartyScreen,
)
import time

PAUSE_MENU_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "pause_menu_signature.png"
)

class PauseMenuSelection(Enum):
    POKEDEX = 15
    POKEMON = 30
    BAG = 45
    CHARACTER = 60
    SAVE = 75
    OPTION = 90
    EXIT = 105

class PauseMenu:
    """Represents the Pokémon Ultra Violet pause menu."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the pause menu is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=PAUSE_MENU_TEMPLATE_PATH,
        )

        return match.found

    def wait_until_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the pause menu becomes visible."""
        wait_until(
            lambda: True if self.is_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet pause menu",
        )

    def open(self) -> None:
        """Open the pause menu and wait until it is visible."""
        self.session.press(
            Button.START,
        )

        self.wait_until_visible()

    def selected_item(self) -> PauseMenuSelection:
        """Return the currently selected pause-menu item."""
        screen = self.session.screenshot()

        cursor_x = 178

        for selection in PauseMenuSelection:
            pixel = screen.pixel(
                cursor_x,
                selection.value,
            )

            if (
                pixel.red == 99
                and pixel.green == 99
                and pixel.blue == 99
            ):
                return selection

        raise RuntimeError(
            "Could not determine the selected pause-menu item."
        )

    def _is_item_selected(
        self,
        expected: PauseMenuSelection,
    ) -> bool | None:
        """Return True when the expected pause-menu item is selected."""
        try:
            selected = self.selected_item()
        except RuntimeError:
            return None

        if selected is expected:
            return True

        return None

    def _move_cursor(
        self,
        button: Button,
        expected: PauseMenuSelection,
        max_attempts: int = 3,
    ) -> None:
        """Press a direction until the expected pause-menu item is selected."""
        for attempt in range(1, max_attempts + 1):
            self.session.press(
                button,
                duration_seconds=0.2,
            )

            try:
                wait_until(
                    lambda: self._is_item_selected(expected),
                    timeout_seconds=1.0,
                    poll_interval_seconds=0.05,
                    description=(
                        f"pause-menu cursor to move to {expected.name}"
                    ),
                )

                return

            except Exception:
                if attempt == max_attempts:
                    raise

                time.sleep(0.2)

    def select(
        self,
        target: PauseMenuSelection,
    ) -> None:
        """Move the pause-menu cursor to the requested item."""
        current = self.selected_item()

        selections = list(PauseMenuSelection)

        current_index = selections.index(current)
        target_index = selections.index(target)

        while current_index < target_index:
            expected = selections[
                current_index + 1
            ]

            self._move_cursor(
                Button.DOWN,
                expected,
            )

            time.sleep(0.25)

            current_index += 1

        while current_index > target_index:
            expected = selections[
                current_index - 1
            ]

            self._move_cursor(
                Button.UP,
                expected,
            )

            time.sleep(0.25)

            current_index -= 1

    def confirm(self) -> None:
        """Open the currently selected pause-menu item."""
        self.session.press(
            Button.A,
        )

    def open_party(self) -> PartyScreen:
        """Open the Pokémon party screen."""
        self.select(
            PauseMenuSelection.POKEMON,
        )

        self.confirm()

        party_screen = PartyScreen(
            session=self.session,
        )

        party_screen.wait_until_visible()

        return party_screen

    def save_game(self) -> None:
        """Open the pause menu and save the game."""
        print("Opening pause menu...")
        self.open()

        print("Selecting SAVE...")
        self.select(
            PauseMenuSelection.SAVE,
        )

        print("Opening SAVE...")
        self.confirm()

        print("Waiting for save confirmation prompt...")
        time.sleep(2.0)

        print("Confirming save...")
        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        print("Waiting for overwrite confirmation...")
        time.sleep(2.0)

        print("Confirming overwrite...")
        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        print("Waiting for game save to complete...")
        time.sleep(3.0)

        print("Game saved successfully.")