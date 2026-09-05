from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import time

from gameboy_automation.emulators import Button
from gameboy_automation.runtime.session import Session
from gameboy_automation.vision.template_matching import (
    find_screen_in_reference,
)

DAY_CARE_TEMPLATE_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "screens"
    / "day_care"
)

DAY_CARE_MAN_TEMPLATE_PATH = (
    DAY_CARE_TEMPLATE_DIRECTORY
    / "man.png"
)

DAY_CARE_MAN_OCCLUDED_TEMPLATE_PATH = (
    DAY_CARE_TEMPLATE_DIRECTORY
    / "man_occluded.png"
)

ROUTE_MAP_PATH = (
    DAY_CARE_TEMPLATE_DIRECTORY
    / "route_map.png"
)

DAY_CARE_APPROACH_X = 222
DAY_CARE_APPROACH_TOLERANCE = 4

DAY_CARE_HATCHING_ROUTE_Y = 50
DAY_CARE_HATCHING_ROUTE_TOLERANCE = 4

class PlayerDirection(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

@dataclass(frozen=True)
class MapPosition:
    x: int
    y: int

@dataclass(frozen=True)
class PlayerState:
    x: int
    y: int
    direction: PlayerDirection
    on_bike: bool


@dataclass(frozen=True)
class DayCareManState:
    x: int
    y: int


class DayCareScreen:
    """Represents the Pokémon Ultra Violet Day Care exterior."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def day_care_man(
        self,
    ) -> DayCareManState:
        """Locate the Day Care Man on screen."""
        screen = self.session.screenshot()

        matches = (
            (
                DAY_CARE_MAN_TEMPLATE_PATH,
                0.95,
            ),
            (
                DAY_CARE_MAN_OCCLUDED_TEMPLATE_PATH,
                0.80,
            ),
        )

        for template_path, confidence in matches:
            match = screen.find_template(
                template_path=template_path,
                confidence=confidence,
            )

            print(
                f"Day Care Man template "
                f"{template_path.name}: "
                f"confidence={match.confidence:.4f}, "
                f"required={confidence:.2f}"
            )

            if match.found:
                print(
                    f"Day Care Man detected using "
                    f"{template_path.name}."
                )

                return DayCareManState(
                    x=match.x,
                    y=match.y,
                )

        raise RuntimeError(
            "Could not locate the Day Care Man."
        )

    def player(
        self,
    ) -> PlayerState:
        """Locate the player and determine direction and bike state."""
        screen = self.session.screenshot()

        template_groups = (
            (False, "on_foot", "full"),
            (True, "bike", "full"),
            (False, "on_foot", "occluded"),
            (True, "bike", "occluded"),
        )

        for on_bike, movement_type, visibility_type in template_groups:
            for direction in PlayerDirection:
                template_path = (
                    DAY_CARE_TEMPLATE_DIRECTORY
                    / "player"
                    / movement_type
                    / visibility_type
                    / f"{direction.value}.png"
                )

                match = screen.find_template(
                    template_path=template_path,
                )

                if match.found:
                    return PlayerState(
                        x=match.x,
                        y=match.y,
                        direction=direction,
                        on_bike=on_bike,
                    )

        raise RuntimeError(
            "Could not locate the player."
        )

    def viewport_position(
        self,
    ) -> MapPosition:
        """Return the current viewport position within the Day Care route map."""
        screen = self.session.screenshot()

        crop_top = 112

        static_screen = screen.crop(
            left=0,
            top=crop_top,
            right=screen.width,
            bottom=screen.height,
        )

        match = find_screen_in_reference(
            screen=static_screen,
            reference_path=ROUTE_MAP_PATH,
            confidence=0.70,
        )

        if not match.found:
            raise RuntimeError(
                "Could not locate the current viewport "
                "within the Day Care route map."
            )

        return MapPosition(
            x=match.x,
            y=match.y - crop_top,
        )

    def player_map_position(
        self,
    ) -> MapPosition:
        """Return the player's position within the Day Care route map."""
        viewport = self.viewport_position()
        player = self.player()

        return MapPosition(
            x=viewport.x + player.x,
            y=viewport.y + player.y,
        )

    def day_care_man_map_position(
        self,
    ) -> MapPosition:
        """Return the Day Care Man's position within the Day Care route map."""
        viewport = self.viewport_position()
        man = self.day_care_man()

        return MapPosition(
            x=viewport.x + man.x,
            y=viewport.y + man.y,
        )

    def is_ready_to_talk_to_man(
        self,
        tolerance: int = 3,
    ) -> bool:
        """Return True when the player is positioned to talk to the Day Care Man."""
        man = self.day_care_man()
        player = self.player()

        relative_x = man.x - player.x
        relative_y = man.y - player.y

        horizontal_match = (
            abs(relative_x) <= tolerance
        )

        vertical_match = (
            abs(relative_y - (-13)) <= tolerance
        )

        facing_up = (
            player.direction is PlayerDirection.UP
        )

        return (
            horizontal_match
            and vertical_match
            and facing_up
        )

    def move_to_day_care_approach(
    self,
    max_attempts: int = 30,
    ) -> None:
        """Move horizontally to the Day Care approach point."""
        print("Moving to Day Care approach point...")

        for attempt in range(1, max_attempts + 1):
            position = self.player_map_position()

            difference_x = (
                DAY_CARE_APPROACH_X - position.x
            )

            print(
                f"Attempt {attempt}: "
                f"player_x={position.x}, "
                f"target_x={DAY_CARE_APPROACH_X}, "
                f"dx={difference_x}"
            )

            if abs(difference_x) <= DAY_CARE_APPROACH_TOLERANCE:
                print(
                    "Day Care horizontal approach position reached."
                )
                return

            if difference_x > 0:
                button = Button.RIGHT
            else:
                button = Button.LEFT

            self.session.press(
                button,
                duration_seconds=0.1,
            )

            time.sleep(0.4)

        raise RuntimeError(
            "Could not reach the Day Care horizontal "
            f"approach position after {max_attempts} attempts."
        )

    def move_to_day_care_man(
        self,
        max_attempts: int = 10,
    ) -> None:
        """Move from the approach point to the Day Care Man."""
        print("Moving to Day Care Man...")

        for attempt in range(1, max_attempts + 1):
            if self.is_ready_to_talk_to_man():
                print("Ready to talk to Day Care Man.")
                return

            print(
                f"Attempt {attempt}: "
                f"moving UP toward Day Care Man..."
            )

            self.session.press(
                Button.UP,
                duration_seconds=0.1,
            )

            time.sleep(0.4)

        raise RuntimeError(
            "Could not reach the Day Care Man "
            f"after {max_attempts} attempts."
        )

    def move_to_hatching_route(
        self,
    ) -> None:
        """Move one tile south from the Day Care Man to the hatching route."""
        print("Moving back to hatching route...")

        before = self.player()

        print(
            f"Before DOWN: "
            f"x={before.x}, "
            f"y={before.y}"
        )

        self.session.press(
            Button.DOWN,
            duration_seconds=0.1,
        )

        time.sleep(0.4)

        after = self.player()

        print(
            f"After DOWN: "
            f"x={after.x}, "
            f"y={after.y}"
        )

        print("Returned to hatching route.")

    def move_to_pokemon_center(
        self,
    ) -> None:
        """Move from the Day Care hatching route into the Pokémon Center."""
        player = self.player()

        if player.on_bike:
            print("Player is on bicycle. Dismounting...")

            self.session.press(
                Button.SELECT,
                duration_seconds=0.2,
            )

            time.sleep(0.5)

            player = self.player()

            if player.on_bike:
                raise RuntimeError(
                    "Failed to dismount bicycle."
                )

            print("Player dismounted bicycle.")

        print("Moving from Day Care route to Pokémon Center...")

        movements = (
            (Button.LEFT, 20),
            (Button.UP, 5),
            (Button.DOWN, 7),
            (Button.RIGHT, 9),
            (Button.UP, 1),
        )

        for button, count in movements:
            for _ in range(count):
                self.session.press(
                    button,
                    duration_seconds=0.2,
                )

                time.sleep(0.5)

        print("Pokémon Center route completed.")

    def move_from_pokemon_center(
        self,
    ) -> None:
        """Move from outside the Pokémon Center back to the Day Care hatching route."""
        print("Moving from Pokémon Center back to Day Care route...")

        movements = (
            (Button.LEFT, 11),
            (Button.UP, 9),
            (Button.DOWN, 2),
            (Button.RIGHT, 6),
        )

        for button, count in movements:
            for _ in range(count):
                self.session.press(
                    button,
                    duration_seconds=0.2,
                )

                time.sleep(0.5)

        print("Returned to Day Care hatching route.")