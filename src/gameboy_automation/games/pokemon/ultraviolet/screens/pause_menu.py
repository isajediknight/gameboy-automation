from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button
from enum import Enum
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PartyScreen,
)

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
            self.session.press(
                Button.DOWN,
            )
            current_index += 1

        while current_index > target_index:
            self.session.press(
                Button.UP,
            )
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