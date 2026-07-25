from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gameboy_automation.pokemon.constants import (
    DIALOGUE_BOX_HEIGHT,
    DIALOGUE_BOX_WIDTH,
    DIALOGUE_BOX_X,
    DIALOGUE_BOX_Y,
)

if TYPE_CHECKING:
    from gameboy_automation.pokemon.game import PokemonGame
    from gameboy_automation.vision.region import Region


@dataclass(frozen=True)
class PokemonRegions:
    """
    Provides named screen regions for a running Pokémon game.
    """

    game: "PokemonGame"

    @property
    def dialogue_box(self) -> "Region":
        """
        Returns the dialogue-box portion of the current screen.
        """
        return self.game.screen.region(
            x=DIALOGUE_BOX_X,
            y=DIALOGUE_BOX_Y,
            width=DIALOGUE_BOX_WIDTH,
            height=DIALOGUE_BOX_HEIGHT,
        )