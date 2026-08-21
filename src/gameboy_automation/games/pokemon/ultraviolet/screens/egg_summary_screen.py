from pathlib import Path

from gameboy_automation.runtime.session import Session
from gameboy_automation.emulators import Button

EGG_SUMMARY_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "egg_summary_signature.png"
)


class EggSummaryScreen:
    """Represents the Pokémon Ultra Violet Egg summary screen."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_visible(self) -> bool:
        """Return True when the Egg summary screen is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=EGG_SUMMARY_TEMPLATE_PATH,
        )

        return match.found

    def close(self) -> None:
        """Return from the Egg summary screen to the party screen."""
        self.session.press(
            Button.B,
        )

        self.session.press(
            Button.B,
        )