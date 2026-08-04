from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from enum import Enum

PARTY_SCREEN_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "party_screen_signature.png"
)

class PartySlot(Enum):
    SLOT_1 = 1
    SLOT_2 = 2
    SLOT_3 = 3
    SLOT_4 = 4
    SLOT_5 = 5
    SLOT_6 = 6

class PartyScreen:
    """Represents the Pokémon Ultra Violet party screen."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the party screen is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=PARTY_SCREEN_TEMPLATE_PATH,
        )

        return match.found

    def wait_until_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the party screen becomes visible."""
        wait_until(
            lambda: True if self.is_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet party screen",
        )

    def selected_slot(self) -> PartySlot:
        """Return the currently selected Pokémon party slot."""
        screen = self.session.screenshot()

        slot_1_pixel = screen.pixel(8, 23)

        if (
            slot_1_pixel.red == 247
            and slot_1_pixel.green == 181
            and slot_1_pixel.blue == 123
        ):
            return PartySlot.SLOT_1

        slot_2_pixel = screen.pixel(120, 10)

        if (
            slot_2_pixel.red == 255
            and slot_2_pixel.green == 115
            and slot_2_pixel.blue == 49
        ):
            return PartySlot.SLOT_2

        raise RuntimeError(
            "Could not determine the selected Pokémon party slot."
        )