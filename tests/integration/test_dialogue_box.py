import bootstrap

from gameboy_automation.emulators.mgba.adapter import MGBAEmulator
from gameboy_automation.pokemon.game import PokemonGame


def test_dialogue_box_is_open(
    mgba_emulator: MGBAEmulator,
) -> None:
    """
    Verifies that the dialogue box can be detected from
    a live emulator screenshot.
    """
    game = PokemonGame(
        emulator=mgba_emulator,
    )

    assert game.dialogue.is_open()