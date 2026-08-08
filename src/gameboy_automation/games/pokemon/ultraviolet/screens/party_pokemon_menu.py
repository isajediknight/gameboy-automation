from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button

PARTY_POKEMON_MENU_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "party_pokemon_menu_signature.png"
)


class PartyPokemonMenu:
    """Represents the action menu for a selected party Pokémon."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the selected Pokémon action menu is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=PARTY_POKEMON_MENU_TEMPLATE_PATH,
        )

        return match.found

    def wait_until_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the selected Pokémon action menu becomes visible."""
        wait_until(
            lambda: True if self.is_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet party Pokémon action menu",
        )

    def confirm(self) -> None:
        """Open the currently selected Pokémon action."""
        self.session.press(
            Button.A,
        )