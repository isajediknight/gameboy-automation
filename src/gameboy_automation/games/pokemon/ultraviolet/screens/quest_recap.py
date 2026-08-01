from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.services.wait import wait_until
from gameboy_automation.emulators import Button

QUEST_RECAP_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "quest_recap_signature.png"
)


class QuestRecap:
    """Represents the Pokémon Ultra Violet quest recap."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the quest recap is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=QUEST_RECAP_TEMPLATE_PATH,
        )

        return match.found

    def wait_until_visible(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        """Wait until the quest recap becomes visible."""
        wait_until(
            self.is_visible,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            description="Pokémon Ultra Violet quest recap",
        )

    def advance(self) -> None:
        """Advance the quest recap by one step."""
        self.session.press(
            Button.A,
        )