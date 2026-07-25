from __future__ import annotations

from gameboy_automation.emulators.base.emulator import Emulator
from gameboy_automation.pokemon.dialogue_box import DialogueBox
from gameboy_automation.vision.screen import Screen
from gameboy_automation.pokemon.regions import PokemonRegions

class PokemonGame:
    """
    Entry point for Pokémon automation.

    This class coordinates higher-level gameplay components such
    as dialogue, battles, menus, inventory, and the overworld.
    """

    def __init__(
        self,
        emulator: Emulator,
    ) -> None:
        self._emulator = emulator
        self._regions = PokemonRegions(
        game=self,
    )
        self._dialogue = DialogueBox(
        game=self,
    )

    @property
    def emulator(self) -> Emulator:
        """
        Returns the emulator used by this game instance.
        """
        return self._emulator

    @property
    def dialogue(self) -> DialogueBox:
        """
        Returns the game's dialogue box.
        """
        return self._dialogue

    @property
    def screen(self) -> Screen:
        """
        Captures and returns the current game screen.
        """
        return self._emulator.screenshot()

    @property
    def regions(self) -> PokemonRegions:
        """
        Returns the collection of named screen regions.
        """
        return self._regions