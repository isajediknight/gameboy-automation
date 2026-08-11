from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
import time
from enum import Enum

from gameboy_automation.emulators import Button

from gameboy_automation.games.pokemon.ultraviolet.vision.number_reader import (
    read_number_auto,
)
from gameboy_automation.vision import screen
from dataclasses import dataclass

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

@dataclass(frozen=True)
class PokemonStats:
    current_hp: int
    max_hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    experience: int
    next_level_experience: int

@dataclass(frozen=True)
class PokemonSummary:
    level: int
    stats: PokemonStats

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

    def level(self) -> int:
        """Return the Pokémon's current level."""
        if not self.is_info_visible():
            raise RuntimeError(
                "Pokémon level can only be read from the Info page."
            )

        screen = self.session.screenshot()

        level_region = screen.crop(
            left=14,
            top=19,
            right=32,
            bottom=29,
        )

        return read_number_auto(
            level_region,
        )

    def current_hp(self) -> int:
        """Return the Pokémon's current HP."""
        current_hp, _ = self.hp()

        return current_hp

    def max_hp(self) -> int:
        """Return the Pokémon's maximum HP."""
        _, max_hp = self.hp()

        return max_hp

    def hp(self) -> tuple[int, int]:
        """Return the Pokémon's current and maximum HP."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon HP can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        return self._read_hp(screen)

    def attack(self) -> int:
        """Return the Pokémon's Attack stat."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon Attack can only be read from the Skills page."
            )

        return self._read_attack(
            self.session.screenshot()
        )

    def defense(self) -> int:
        """Return the Pokémon's Defense stat."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon Defense can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        defense_region = screen.crop(
            left=219,
            top=51,
            right=237,
            bottom=61,
        )

        return read_number_auto(
            defense_region,
        )

    def special_attack(self) -> int:
        """Return the Pokémon's Special Attack stat."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon Special Attack can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        special_attack_region = screen.crop(
            left=219,
            top=64,
            right=237,
            bottom=74,
        )

        return read_number_auto(
            special_attack_region,
        )

    def special_defense(self) -> int:
        """Return the Pokémon's Special Defense stat."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon Special Defense can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        special_defense_region = screen.crop(
            left=219,
            top=77,
            right=237,
            bottom=87,
        )

        return read_number_auto(
            special_defense_region,
        )

    def speed(self) -> int:
        """Return the Pokémon's Speed stat."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon Speed can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        speed_region = screen.crop(
            left=219,
            top=91,
            right=237,
            bottom=101,
        )

        return read_number_auto(
            speed_region,
        )

    def experience(self) -> int:
        """Return the Pokémon's experience points."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon experience can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        experience_region = screen.crop(
            left=190,
            top=104,
            right=240,
            bottom=114,
        )

        return read_number_auto(
            experience_region,
        )

    def next_level_experience(self) -> int:
        """Return the experience points required to reach the next level."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon next-level experience can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        next_level_experience_region = screen.crop(
            left=208,
            top=116,
            right=240,
            bottom=126,
        )

        return read_number_auto(
            next_level_experience_region,
        )

    def stats(self) -> PokemonStats:
        """Return numeric Pokémon stats from one Skills-page screenshot."""
        if not self.is_skills_visible():
            raise RuntimeError(
                "Pokémon stats can only be read from the Skills page."
            )

        screen = self.session.screenshot()

        current_hp, max_hp = self._read_hp(screen)

        return PokemonStats(
            current_hp=current_hp,
            max_hp=max_hp,
            attack=self._read_attack(screen),
            defense=self._read_defense(screen),
            special_attack=self._read_special_attack(screen),
            special_defense=self._read_special_defense(screen),
            speed=self._read_speed(screen),
            experience=self._read_experience(screen),
            next_level_experience=self._read_next_level_experience(
                screen
            ),
        )
    
    def _read_hp(self,screen,) -> tuple[int, int]:
        """Read current and maximum HP from a Skills-page screenshot."""
        hp_region = screen.crop(
            left=195,
            top=20,
            right=240,
            bottom=30,
        )

        separator_match = hp_region.find_template(
            template_path=(
                Path(__file__).resolve().parents[1]
                / "assets"
                / "templates"
                / "hp_separator.png"
            ),
        )

        if not separator_match.found:
            raise RuntimeError(
                "Could not locate the HP separator."
            )

        current_hp_region = hp_region.crop(
            left=0,
            top=0,
            right=separator_match.x,
            bottom=hp_region.height,
        )

        max_hp_region = hp_region.crop(
            left=separator_match.x + separator_match.width,
            top=0,
            right=hp_region.width,
            bottom=hp_region.height,
        )

        return (
            read_number_auto(current_hp_region),
            read_number_auto(max_hp_region),
        )


    def _read_attack(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=219,
                top=39,
                right=237,
                bottom=49,
            )
        )


    def _read_defense(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=219,
                top=51,
                right=237,
                bottom=61,
            )
        )


    def _read_special_attack(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=219,
                top=64,
                right=237,
                bottom=74,
            )
        )


    def _read_special_defense(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=219,
                top=77,
                right=237,
                bottom=87,
            )
        )


    def _read_speed(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=219,
                top=91,
                right=237,
                bottom=101,
            )
        )


    def _read_experience(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=190,
                top=104,
                right=240,
                bottom=114,
            )
        )


    def _read_next_level_experience(self, screen) -> int:
        return read_number_auto(
            screen.crop(
                left=208,
                top=116,
                right=240,
                bottom=126,
            )
        )

    def read_summary(self) -> PokemonSummary:
        """
        Read the Pokémon's numeric summary.

        The method navigates between the Info and Skills pages as needed.
        """
        self.go_to(
            PokemonSummaryPage.INFO,
        )

        level = self.level()

        self.go_to(
            PokemonSummaryPage.SKILLS,
        )

        stats = self.stats()

        return PokemonSummary(
            level=level,
            stats=stats,
        )