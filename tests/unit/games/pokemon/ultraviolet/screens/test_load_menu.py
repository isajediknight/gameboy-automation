from unittest.mock import Mock

import bootstrap

from gameboy_automation.emulators import Button
from gameboy_automation.games.pokemon.ultraviolet.screens.load_menu import (
    LOAD_MENU_TEMPLATE_PATH,
    LoadMenu,
)


def test_is_visible_returns_true_when_template_is_found():
    match = Mock()
    match.found = True

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    load_menu = LoadMenu(
        session=session,
    )

    assert load_menu.is_visible() is True

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=LOAD_MENU_TEMPLATE_PATH,
    )

def test_is_visible_returns_false_when_template_is_not_found():
    match = Mock()
    match.found = False

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    load_menu = LoadMenu(
        session=session,
    )

    assert load_menu.is_visible() is False

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=LOAD_MENU_TEMPLATE_PATH,
    )

def test_wait_until_visible_waits_for_load_menu(monkeypatch):
    load_menu = LoadMenu(
        session=Mock(),
    )

    wait_until_mock = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.load_menu.wait_until",
        wait_until_mock,
    )

    load_menu.wait_until_visible(
        timeout_seconds=5.0,
        poll_interval_seconds=0.25,
    )

    wait_until_mock.assert_called_once_with(
        load_menu.is_visible,
        timeout_seconds=5.0,
        poll_interval_seconds=0.25,
        description="Pokémon Ultra Violet load menu",
    )

def test_continue_game_presses_a_button():
    session = Mock()

    load_menu = LoadMenu(
        session=session,
    )

    load_menu.continue_game()

    session.press.assert_called_once_with(
        Button.A,
    )