from unittest.mock import Mock

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (
    PAUSE_MENU_TEMPLATE_PATH,
    PauseMenu,
    PauseMenuSelection,
)
from gameboy_automation.emulators import Button
from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PartyScreen,
)

def test_is_visible_returns_true_when_template_is_found():
    match = Mock()
    match.found = True

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    pause_menu = PauseMenu(
        session=session,
    )

    assert pause_menu.is_visible() is True

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=PAUSE_MENU_TEMPLATE_PATH,
    )


def test_is_visible_returns_false_when_template_is_not_found():
    match = Mock()
    match.found = False

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    pause_menu = PauseMenu(
        session=session,
    )

    assert pause_menu.is_visible() is False

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=PAUSE_MENU_TEMPLATE_PATH,
    )

def test_wait_until_visible_waits_for_pause_menu(monkeypatch):
    pause_menu = PauseMenu(
        session=Mock(),
    )

    wait_until_mock = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu.wait_until",
        wait_until_mock,
    )

    pause_menu.wait_until_visible(
        timeout_seconds=5.0,
        poll_interval_seconds=0.25,
    )

    wait_until_mock.assert_called_once()

    _, kwargs = wait_until_mock.call_args

    assert kwargs == {
        "timeout_seconds": 5.0,
        "poll_interval_seconds": 0.25,
        "description": "Pokémon Ultra Violet pause menu",
    }

def test_open_presses_start_and_waits_until_visible():
    session = Mock()

    pause_menu = PauseMenu(
        session=session,
    )

    pause_menu.wait_until_visible = Mock()

    pause_menu.open()

    session.press.assert_called_once_with(
        Button.START,
    )

    pause_menu.wait_until_visible.assert_called_once_with()

def test_selected_item_returns_pokemon():
    session = Mock()

    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=255, green=255, blue=255),
        Mock(red=99, green=99, blue=99),
    ]

    session.screenshot.return_value = screen

    pause_menu = PauseMenu(
        session=session,
    )

    result = pause_menu.selected_item()

    assert result is PauseMenuSelection.POKEMON

def test_select_moves_down_to_pokemon():
    session = Mock()

    pause_menu = PauseMenu(
        session=session,
    )

    pause_menu.selected_item = Mock(
        return_value=PauseMenuSelection.POKEDEX,
    )

    pause_menu.select(
        PauseMenuSelection.POKEMON,
    )

    session.press.assert_called_once_with(
        Button.DOWN,
    )

def test_select_moves_up_to_pokemon():
    session = Mock()

    pause_menu = PauseMenu(
        session=session,
    )

    pause_menu.selected_item = Mock(
        return_value=PauseMenuSelection.BAG,
    )

    pause_menu.select(
        PauseMenuSelection.POKEMON,
    )

    session.press.assert_called_once_with(
        Button.UP,
    )

def test_select_moves_multiple_steps_up_to_pokemon():
    session = Mock()

    pause_menu = PauseMenu(
        session=session,
    )

    pause_menu.selected_item = Mock(
        return_value=PauseMenuSelection.EXIT,
    )

    pause_menu.select(
        PauseMenuSelection.POKEMON,
    )

    assert session.press.call_count == 5

    session.press.assert_called_with(
        Button.UP,
    )

def test_confirm_presses_a_button():
    session = Mock()

    pause_menu = PauseMenu(
        session=session,
    )

    pause_menu.confirm()

    session.press.assert_called_once_with(
        Button.A,
    )

def test_open_party_selects_pokemon_and_waits_for_party_screen(monkeypatch):
    session = Mock()

    pause_menu = PauseMenu(
        session=session,
    )

    pause_menu.select = Mock()
    pause_menu.confirm = Mock()

    party_screen = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu.PartyScreen",
        Mock(return_value=party_screen),
    )

    result = pause_menu.open_party()

    pause_menu.select.assert_called_once_with(
        PauseMenuSelection.POKEMON,
    )

    pause_menu.confirm.assert_called_once_with()

    party_screen.wait_until_visible.assert_called_once_with()

    assert result is party_screen