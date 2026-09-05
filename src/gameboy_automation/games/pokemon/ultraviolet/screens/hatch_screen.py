from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.emulators import Button
from gameboy_automation.services.wait import wait_until
import time

HATCH_HUH_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "screens"
    / "hatch"
    / "huh.png"
)

HATCH_HATCHED_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "screens"
    / "hatch"
    / "hatched.png"
)

HATCH_NICKNAME_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "screens"
    / "hatch"
    / "nickname.png"
)

POLL_INTERVAL_SECONDS = 0.1

class HatchScreen:
    """Represents the start of the Pokémon Ultra Violet hatch sequence."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the hatch sequence has started."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=HATCH_HUH_TEMPLATE_PATH,
        )

        return match.found

    def move_until_hatch(
        self,
        button: Button,
        duration_seconds: float,
    ) -> bool:
        """Move in one direction until the hatch sequence starts or time expires."""
        print(
            f"Holding {button.name} for up to "
            f"{duration_seconds:.1f} seconds..."
        )

        self.session.key_down(
            button,
        )

        try:
            deadline = time.monotonic() + duration_seconds

            while time.monotonic() < deadline:
                if self.is_visible():
                    print("Hatch sequence detected!")
                    return True

                time.sleep(
                    POLL_INTERVAL_SECONDS,
                )

            return False

        finally:
            self.session.key_up(
                button,
            )
    
    def wait_for_hatch(
        self,
        move_seconds: float,
    ) -> None:
        """Move back and forth until the hatch sequence begins."""
        hatch_detected = False

        while not hatch_detected:
            hatch_detected = self.move_until_hatch(
                Button.RIGHT,
                move_seconds,
            )

            if hatch_detected:
                return

            hatch_detected = self.move_until_hatch(
                Button.LEFT,
                move_seconds,
            )
    
    def is_hatched_visible(self) -> bool:
        """Return True when the hatch-complete dialogue is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=HATCH_HATCHED_TEMPLATE_PATH,
        )

        return match.found


    def is_nickname_visible(self) -> bool:
        """Return True when the nickname prompt is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=HATCH_NICKNAME_TEMPLATE_PATH,
        )

        return match.found

    def finish_hatch(self) -> None:
        """Advance through the hatch sequence and decline a nickname."""
        print("Advancing from Huh?...")
        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        print("Waiting for hatch-complete dialogue...")
        wait_until(
            self.is_hatched_visible,
            timeout_seconds=20.0,
            poll_interval_seconds=0.1,
            description="Pokémon hatch-complete dialogue",
        )

        print("Hatch-complete dialogue detected.")

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        print("Waiting for nickname prompt...")
        wait_until(
            self.is_nickname_visible,
            timeout_seconds=10.0,
            poll_interval_seconds=0.1,
            description="Pokémon nickname prompt",
        )

        print("Nickname prompt detected.")
        print("Waiting for nickname menu to become ready...")

        time.sleep(20.0)

        print("Selecting NO...")

        self.session.press(
            Button.DOWN,
            duration_seconds=0.2,
        )

        print("Declining nickname...")

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )