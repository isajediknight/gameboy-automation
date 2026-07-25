from __future__ import annotations

from typing import TYPE_CHECKING

from gameboy_automation.emulators.base.button import Button
from gameboy_automation.pokemon.constants import CONTINUE_ARROW_TEMPLATE

if TYPE_CHECKING:
    from gameboy_automation.pokemon.game import PokemonGame


class DialogueBox:
    """
    Represents the dialogue box displayed during gameplay.
    """

    def __init__(
        self,
        game: "PokemonGame",
    ) -> None:
        self._game = game

    @property
    def region(self):
        """
        Returns the dialogue-box portion of the current screen.
        """
        return self._game.regions.dialogue_box

    def is_open(
        self,
        confidence: float = 0.95,
    ) -> bool:
        """
        Returns whether the game is waiting for dialogue input.
        """
        match = self.region.find_template(
            template_path=CONTINUE_ARROW_TEMPLATE,
            confidence=confidence,
        )

        return match.found

    def advance(self) -> None:
        """
        Advances the current dialogue.
        """
        self._game.emulator.press(Button.A)