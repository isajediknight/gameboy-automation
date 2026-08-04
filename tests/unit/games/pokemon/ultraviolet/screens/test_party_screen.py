from unittest.mock import Mock

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PARTY_SCREEN_TEMPLATE_PATH,
    PartyScreen,
    PartySlot,
)


def test_is_visible_returns_true_when_template_is_found():
    match = Mock()
    match.found = True

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.is_visible() is True

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=PARTY_SCREEN_TEMPLATE_PATH,
    )


def test_is_visible_returns_false_when_template_is_not_found():
    match = Mock()
    match.found = False

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.is_visible() is False

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=PARTY_SCREEN_TEMPLATE_PATH,
    )

def test_wait_until_visible_waits_for_party_screen(monkeypatch):
    party_screen = PartyScreen(
        session=Mock(),
    )

    wait_until_mock = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.party_screen.wait_until",
        wait_until_mock,
    )

    party_screen.wait_until_visible(
        timeout_seconds=5.0,
        poll_interval_seconds=0.25,
    )

    wait_until_mock.assert_called_once()

    _, kwargs = wait_until_mock.call_args

    assert kwargs == {
        "timeout_seconds": 5.0,
        "poll_interval_seconds": 0.25,
        "description": "Pokémon Ultra Violet party screen",
    }

def test_selected_slot_returns_slot_1():
    session = Mock()
    screen = Mock()

    screen.pixel.return_value = Mock(
        red=255,
        green=255,
        blue=255,
    )

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_1


def test_selected_slot_returns_slot_2():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=0, green=0, blue=0),
        Mock(red=255, green=255, blue=255),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_2