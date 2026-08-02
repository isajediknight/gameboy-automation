from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button

LOAD_MENU_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "load_menu_signature.png"
)


class LoadMenu:
    """Represents the Pokémon Ultra Violet load menu."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the load-menu template is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=LOAD_MENU_TEMPLATE_PATH,
        )

        return match.found

    def wait_until_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the load menu becomes visible."""
        wait_until(
            lambda: True if self.is_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet load menu",
        )

    def continue_game(self) -> None:
        """
        Continue the currently selected saved game.
        """
        self.session.press(
            Button.A,
            duration_seconds=0.5,
        )

    def test_continue_game_presses_a_button():
        session = Mock()

        load_menu = LoadMenu(
            session=session,
        )

        load_menu.continue_game()

        session.press.assert_called_once_with(
            Button.A,
        )