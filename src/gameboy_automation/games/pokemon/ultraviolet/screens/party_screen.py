from enum import Enum
from pathlib import Path
import time

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button

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

        selected_border_color = (
            255,
            115,
            49,
        )

        slot_1_pixel = screen.pixel(
            22,
            26,
        )

        if (
            slot_1_pixel.red,
            slot_1_pixel.green,
            slot_1_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_1

        slot_2_pixel = screen.pixel(
            120,
            10,
        )

        if (
            slot_2_pixel.red,
            slot_2_pixel.green,
            slot_2_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_2

        slot_3_pixel = screen.pixel(
            104,
            34,
        )

        if (
            slot_3_pixel.red,
            slot_3_pixel.green,
            slot_3_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_3

        slot_4_pixel = screen.pixel(
            103,
            58,
        )

        if (
            slot_4_pixel.red,
            slot_4_pixel.green,
            slot_4_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_4

        slot_5_pixel = screen.pixel(
            103,
            82,
        )

        if (
            slot_5_pixel.red,
            slot_5_pixel.green,
            slot_5_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_5

        slot_6_pixel = screen.pixel(
            103,
            106,
        )

        if (
            slot_6_pixel.red,
            slot_6_pixel.green,
            slot_6_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_6

        raise RuntimeError(
            "Could not determine the selected Pokémon party slot."
        )

    def party_size(self) -> int:
        """Return the number of Pokémon currently in the party."""
        screen = self.session.screenshot()

        slot_coordinates = [
            (150, 20),
            (150, 44),
            (150, 68),
            (150, 92),
            (150, 116),
        ]

        slot_colors = []

        for x, y in slot_coordinates:
            pixel = screen.pixel(
                x,
                y,
            )

            slot_colors.append(
                (
                    pixel.red,
                    pixel.green,
                    pixel.blue,
                )
            )

        party_size = 1

        for index, color in enumerate(slot_colors):
            remaining_colors = slot_colors[index:]

            if len(remaining_colors) >= 2 and all(
                remaining_color == color
                for remaining_color in remaining_colors
            ):
                break

            party_size += 1

        return party_size

    def _is_slot_selected(
        self,
        expected: PartySlot,
    ) -> bool | None:
        """Return True when the expected slot is selected."""
        try:
            selected = self.selected_slot()
        except RuntimeError:
            return None

        if selected is expected:
            return True

        return None

    def select(
        self,
        target: PartySlot,
    ) -> None:
        """Move the party cursor to the requested occupied slot."""
        party_size = self.party_size()

        if target.value > party_size:
            raise ValueError(
                f"Cannot select {target.name}; "
                f"party contains {party_size} Pokémon."
            )

        current = self.selected_slot()

        while current.value < target.value:
            expected = PartySlot(current.value + 1)

            self.session.press(
                Button.DOWN,
            )

            wait_until(
                lambda: self._is_slot_selected(expected),
                timeout_seconds=5.0,
                poll_interval_seconds=0.05,
                description=f"party cursor to move to {expected.name}",
            )

            time.sleep(0.25)

            current = expected

            current = expected

        while current.value > target.value:
            expected = PartySlot(current.value - 1)

            self.session.press(
                Button.UP,
            )

            wait_until(
                lambda: self._is_slot_selected(expected),
                timeout_seconds=5.0,
                poll_interval_seconds=0.05,
                description=f"party cursor to move to {expected.name}",
            )

            time.sleep(0.25)

            current = expected

            current = expected