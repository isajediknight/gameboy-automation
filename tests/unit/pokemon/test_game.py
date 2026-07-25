import bootstrap

from unittest.mock import Mock
from gameboy_automation.emulators.base.button import Button
from gameboy_automation.emulators.base.emulator import Emulator
from gameboy_automation.pokemon.dialogue_box import DialogueBox
from gameboy_automation.pokemon.game import PokemonGame
from PIL import Image

from gameboy_automation.vision.screen import Screen
from gameboy_automation.pokemon.regions import PokemonRegions


def test_game_exposes_emulator() -> None:
    emulator = Mock(spec=Emulator)

    game = PokemonGame(emulator=emulator)

    assert game.emulator is emulator


def test_game_exposes_dialogue_box() -> None:
    emulator = Mock(spec=Emulator)

    game = PokemonGame(emulator=emulator)

    assert isinstance(game.dialogue, DialogueBox)


def test_game_returns_same_dialogue_box_instance() -> None:
    emulator = Mock(spec=Emulator)

    game = PokemonGame(emulator=emulator)

    assert game.dialogue is game.dialogue


def test_dialogue_advance_presses_a() -> None:
    emulator = Mock(spec=Emulator)

    game = PokemonGame(emulator=emulator)

    game.dialogue.advance()

    emulator.press.assert_called_once_with(Button.A)


def test_game_screen_returns_emulator_screenshot() -> None:
    emulator = Mock(spec=Emulator)

    expected_screen = Screen(
        Image.new(
            mode="RGB",
            size=(240, 160),
            color=(255, 255, 255),
        )
    )

    emulator.screenshot.return_value = expected_screen

    game = PokemonGame(emulator=emulator)

    actual_screen = game.screen

    assert actual_screen is expected_screen
    emulator.screenshot.assert_called_once_with()


def test_dialogue_region_uses_current_game_screen() -> None:
    emulator = Mock(spec=Emulator)

    screen = Screen(
        Image.new(
            mode="RGB",
            size=(240, 160),
            color=(255, 255, 255),
        )
    )

    emulator.screenshot.return_value = screen

    game = PokemonGame(emulator=emulator)

    region = game.dialogue.region

    assert region.screen is screen
    assert region.x == 0
    assert region.y == 96
    assert region.width == 240
    assert region.height == 64

    emulator.screenshot.assert_called_once_with()

def test_game_exposes_regions() -> None:
    emulator = Mock(spec=Emulator)

    game = PokemonGame(emulator=emulator)

    assert isinstance(game.regions, PokemonRegions)


def test_game_returns_same_regions_instance() -> None:
    emulator = Mock(spec=Emulator)

    game = PokemonGame(emulator=emulator)

    assert game.regions is game.regions