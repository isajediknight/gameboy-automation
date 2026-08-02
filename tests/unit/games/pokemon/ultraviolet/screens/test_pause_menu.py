from unittest.mock import Mock

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.pause_menu import (
    PAUSE_MENU_TEMPLATE_PATH,
    PauseMenu,
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