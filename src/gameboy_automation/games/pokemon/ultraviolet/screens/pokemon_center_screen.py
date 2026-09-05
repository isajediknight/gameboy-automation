from pathlib import Path
import time

from gameboy_automation.emulators import Button
from gameboy_automation.runtime.session import Session
from gameboy_automation.games.pokemon.ultraviolet.screens.pc_screen import (
    PCScreen,
)

POKEMON_CENTER_TEMPLATE_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "screens"
    / "pokemon_center"
)

PC_TEMPLATE_PATH = (
    POKEMON_CENTER_TEMPLATE_DIRECTORY
    / "pc.png"
)

PLAYER_UP_TEMPLATE_PATH = (
    POKEMON_CENTER_TEMPLATE_DIRECTORY
    .parent
    / "day_care"
    / "player"
    / "on_foot"
    / "full"
    / "up.png"
)


class PokemonCenterScreen:
    """Represents the interior of a Pokémon Center."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_ready_to_use_pc(
        self,
        tolerance: int = 2,
    ) -> bool:
        """Return True when the player is positioned to use the PC."""
        screen = self.session.screenshot()

        pc_match = screen.find_template(
            template_path=PC_TEMPLATE_PATH,
            confidence=0.75,
        )

        if not pc_match.found:
            return False

        player_match = screen.find_template(
            template_path=PLAYER_UP_TEMPLATE_PATH,
            confidence=0.90,
        )

        if not player_match.found:
            return False

        relative_x = (
            pc_match.x - player_match.x
        )

        relative_y = (
            pc_match.y - player_match.y
        )

        horizontal_match = (
            abs(relative_x - (-1)) <= tolerance
        )

        vertical_match = (
            abs(relative_y - (-20)) <= tolerance
        )

        return (
            horizontal_match
            and vertical_match
        )

    def move_to_pc(self) -> None:
        """Move from the Pokémon Center entrance to the PC."""
        for button in (
            Button.UP,
            Button.UP,
            Button.UP,
            Button.UP,
            Button.RIGHT,
            Button.RIGHT,
            Button.RIGHT,
            Button.RIGHT,
            Button.RIGHT,
            Button.UP,
            Button.UP,
            Button.UP,
            Button.LEFT,
            Button.LEFT,
            Button.UP,
            Button.UP,
        ):
            self.session.press(
                button,
                duration_seconds=0.2,
            )

            time.sleep(0.5)

        if not self.is_ready_to_use_pc():
            raise RuntimeError(
                "Failed to reach the Pokémon Center PC."
            )

    def move_to_exit(
        self,
    ) -> None:
        """Move from the PC to the Pokémon Center exit."""
        movements = (
            (Button.DOWN, 2),
            (Button.RIGHT, 5),
            (Button.LEFT, 7),
            (Button.DOWN, 6),
        )

        for button, count in movements:
            for _ in range(count):
                self.session.press(
                    button,
                    duration_seconds=0.2,
                )

                time.sleep(0.5)

        print("Exited Pokémon Center.")

    def deposit_all_except_first(
        self,
    ) -> None:
        """Deposit party slots 2 through 6 and return to the Pokémon Center exit."""
        print("Moving to PC to deposit Pokémon...")

        self.move_to_pc()

        time.sleep(3.0)

        pc_screen = PCScreen(
            session=self.session,
        )

        pc_screen.open_deposit_party()

        pc_screen.deposit_all_except_first()

        pc_screen.exit_to_overworld()

        self.move_to_exit()

        print(
            "Pokémon deposited and Pokémon Center "
            "exit reached."
        )
