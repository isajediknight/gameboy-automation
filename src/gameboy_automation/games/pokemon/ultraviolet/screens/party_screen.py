from enum import Enum
from pathlib import Path
import time

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button

from gameboy_automation.games.pokemon.ultraviolet.screens.party_pokemon_menu import (
    PartyPokemonMenu,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.egg_summary_screen import (
    EggSummaryScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen import (
    PokemonSummaryScreen,
)

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

    def is_egg(
        self,
        slot: PartySlot,
    ) -> bool:
        """Return True when the requested party slot contains an Egg."""
        self.select(
            slot,
        )

        pokemon_menu = self.open_selected()

        pokemon_menu.confirm()

        egg_summary = EggSummaryScreen(
            session=self.session,
        )

        pokemon_summary = PokemonSummaryScreen(
            session=self.session,
        )

        def summary_is_visible() -> bool | None:
            if egg_summary.is_visible():
                return True

            if pokemon_summary.is_info_visible():
                return True

            return None

        wait_until(
            summary_is_visible,
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
            description="Egg or Pokémon summary screen",
        )

        is_egg = egg_summary.is_visible()

        print(f"Egg detected: {is_egg}")

        for press_number in range(1, 6):
            print(f"Pressing B #{press_number}...")

            self.session.press(
                Button.B,
                duration_seconds=0.2,
            )

            time.sleep(1.0)

            party_visible = self.is_visible()
            menu_visible = pokemon_menu.is_visible()

            print(
                f"After B #{press_number}: "
                f"party={party_visible}, "
                f"pokemon_menu={menu_visible}"
            )

            if party_visible:
                print(
                    f"Returned to party after "
                    f"{press_number} B presses."
                )

                return is_egg

        raise RuntimeError(
            "Could not return to the party screen "
            "after 5 B presses."
        )

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
            104,
            57,
        )

        if (
            slot_4_pixel.red,
            slot_4_pixel.green,
            slot_4_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_4

        slot_5_pixel = screen.pixel(
            104,
            81,
        )

        if (
            slot_5_pixel.red,
            slot_5_pixel.green,
            slot_5_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_5

        slot_6_pixel = screen.pixel(
            104,
            105,
        )

        if (
            slot_6_pixel.red,
            slot_6_pixel.green,
            slot_6_pixel.blue,
        ) == selected_border_color:
            return PartySlot.SLOT_6

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

        empty_slot_color = (
            57,
            140,
            140,
        )

        slot_coordinates = [
            (150, 20),
            (150, 44),
            (150, 68),
            (150, 92),
            (150, 116),
        ]

        party_size = 1

        for x, y in slot_coordinates:
            pixel = screen.pixel(
                x,
                y,
            )

            pixel_color = (
                pixel.red,
                pixel.green,
                pixel.blue,
            )

            if pixel_color == empty_slot_color:
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

    def _wait_for_selected_slot(
        self,
        max_attempts: int = 10,
    ) -> PartySlot:
        """Wait until the currently selected party slot can be detected."""
        for attempt in range(1, max_attempts + 1):
            try:
                return self.selected_slot()

            except RuntimeError:
                if attempt == max_attempts:
                    raise

                time.sleep(0.1)

        raise RuntimeError(
            "Could not determine the selected Pokémon party slot."
        )

    def _move_cursor(
        self,
        button: Button,
        expected: PartySlot,
        max_attempts: int = 3,
    ) -> None:
        """Press a direction until the expected party slot is selected."""
        for attempt in range(1, max_attempts + 1):
            self.session.press(
                button,
                duration_seconds=0.2,
            )

            try:
                wait_until(
                    lambda: self._is_slot_selected(expected),
                    timeout_seconds=1.0,
                    poll_interval_seconds=0.05,
                    description=(
                        f"party cursor to move to {expected.name}"
                    ),
                )

                return

            except Exception:
                if attempt == max_attempts:
                    raise

                time.sleep(0.2)

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

        current = self._wait_for_selected_slot()

        while current.value < target.value:
            expected = PartySlot(
                current.value + 1
            )

            self._move_cursor(
                Button.DOWN,
                expected,
            )

            time.sleep(0.25)

            current = expected

        while current.value > target.value:
            expected = PartySlot(
                current.value - 1
            )

            self._move_cursor(
                Button.UP,
                expected,
            )

            time.sleep(0.25)

            current = expected

    def open_selected(self) -> PartyPokemonMenu:
        """Open the action menu for the currently selected Pokémon."""
        self.session.press(
            Button.A,
        )

        menu = PartyPokemonMenu(
            session=self.session,
        )

        menu.wait_until_visible()

        return menu