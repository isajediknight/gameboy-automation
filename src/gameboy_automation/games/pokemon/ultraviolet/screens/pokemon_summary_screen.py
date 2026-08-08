from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
import time
from enum import Enum

from gameboy_automation.emulators import Button

POKEMON_SUMMARY_INFO_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "pokemon_summary_info_signature.png"
)

POKEMON_SUMMARY_SKILLS_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "pokemon_summary_skills_signature.png"
)

POKEMON_SUMMARY_MOVES_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "pokemon_summary_moves_signature.png"
)

class PokemonSummaryPage(Enum):
    INFO = 1
    SKILLS = 2
    MOVES = 3

class PokemonSummaryScreen:
    """Represents the Pokémon Ultra Violet Pokémon summary screen."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_info_visible(self) -> bool:
        """Return True when the Pokémon Info page is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=POKEMON_SUMMARY_INFO_TEMPLATE_PATH,
        )

        return match.found

    def wait_until_info_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the Pokémon Info page becomes visible."""
        wait_until(
            lambda: True if self.is_info_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet Pokémon Info page",
        )

    def is_skills_visible(self) -> bool:
        """Return True when the Pokémon Skills page is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=POKEMON_SUMMARY_SKILLS_TEMPLATE_PATH,
        )

        return match.found


    def wait_until_skills_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the Pokémon Skills page becomes visible."""
        wait_until(
            lambda: True if self.is_skills_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet Pokémon Skills page",
        )


    def is_moves_visible(self) -> bool:
        """Return True when the Known Moves page is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=POKEMON_SUMMARY_MOVES_TEMPLATE_PATH,
        )

        return match.found


    def wait_until_moves_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the Known Moves page becomes visible."""
        wait_until(
            lambda: True if self.is_moves_visible() else None,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet Known Moves page",
        )

    def current_page(self) -> PokemonSummaryPage:
        """Return the currently visible Pokémon summary page."""
        if self.is_info_visible():
            return PokemonSummaryPage.INFO

        if self.is_skills_visible():
            return PokemonSummaryPage.SKILLS

        if self.is_moves_visible():
            return PokemonSummaryPage.MOVES

        raise RuntimeError(
            "Could not determine the current Pokémon summary page."
        )

    def go_to(
        self,
        target: PokemonSummaryPage,
    ) -> None:
        """Navigate to the requested Pokémon summary page."""
        current = self.current_page()

        if current is target:
            return

        if current is PokemonSummaryPage.INFO:
            time.sleep(1)

        while current.value < target.value:
            self.session.press(
                Button.RIGHT,
                duration_seconds=0.5,
            )

            current = PokemonSummaryPage(
                current.value + 1,
            )

            if current is PokemonSummaryPage.SKILLS:
                self.wait_until_skills_visible()
            elif current is PokemonSummaryPage.MOVES:
                self.wait_until_moves_visible()

        while current.value > target.value:
            self.session.press(
                Button.LEFT,
                duration_seconds=0.5,
            )

            current = PokemonSummaryPage(
                current.value - 1,
            )

            if current is PokemonSummaryPage.SKILLS:
                self.wait_until_skills_visible()
            elif current is PokemonSummaryPage.INFO:
                self.wait_until_info_visible()