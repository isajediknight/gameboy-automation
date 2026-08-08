from unittest.mock import Mock
import pytest
import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.party_screen import (
    PARTY_SCREEN_TEMPLATE_PATH,
    PartyScreen,
    PartySlot,
)
from gameboy_automation.emulators import Button


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
        green=115,
        blue=49,
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
        Mock(red=74, green=74, blue=99),
        Mock(red=255, green=115, blue=49),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_2

def test_selected_slot_returns_slot_3():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=255, green=115, blue=49),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_3


def test_selected_slot_returns_slot_4():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=255, green=115, blue=49),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_4


def test_selected_slot_returns_slot_5():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=255, green=115, blue=49),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_5


def test_selected_slot_returns_slot_6():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=74, green=74, blue=99),
        Mock(red=255, green=115, blue=49),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.selected_slot() is PartySlot.SLOT_6

def test_party_size_returns_3():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=57, green=148, blue=222),  # slot 2 occupied
        Mock(red=255, green=255, blue=255),  # slot 3 occupied
        Mock(red=57, green=140, blue=140),  # slot 4 empty
        Mock(red=57, green=140, blue=140),  # slot 5 empty
        Mock(red=57, green=140, blue=140),  # slot 6 empty
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.party_size() == 3

def test_party_size_returns_6():
    session = Mock()
    screen = Mock()

    screen.pixel.side_effect = [
        Mock(red=57, green=148, blue=222),
        Mock(red=255, green=255, blue=255),
        Mock(red=115, green=115, blue=115),
        Mock(red=57, green=148, blue=222),
        Mock(red=82, green=82, blue=82),
    ]

    session.screenshot.return_value = screen

    party_screen = PartyScreen(
        session=session,
    )

    assert party_screen.party_size() == 6

def test_select_moves_down_to_target_slot(monkeypatch):
    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.party_screen.time.sleep",
        Mock(),
    )

    session = Mock()

    party_screen = PartyScreen(
        session=session,
    )

    party_screen.party_size = Mock(
        return_value=6,
    )

    party_screen.selected_slot = Mock(
        side_effect=[
            PartySlot.SLOT_2,
            PartySlot.SLOT_3,
            PartySlot.SLOT_4,
        ]
    )

    party_screen.select(
        PartySlot.SLOT_4,
    )

    assert session.press.call_count == 2

    session.press.assert_called_with(
        Button.DOWN,
    )


def test_select_moves_up_to_target_slot(monkeypatch):
    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.party_screen.time.sleep",
        Mock(),
    )

    session = Mock()

    party_screen = PartyScreen(
        session=session,
    )

    party_screen.party_size = Mock(
        return_value=6,
    )

    party_screen.selected_slot = Mock(
        side_effect=[
            PartySlot.SLOT_5,
            PartySlot.SLOT_4,
            PartySlot.SLOT_3,
        ]
    )

    party_screen.select(
        PartySlot.SLOT_3,
    )

    assert session.press.call_count == 2

    session.press.assert_called_with(
        Button.UP,
    )


def test_select_rejects_slot_beyond_party_size():
    session = Mock()

    party_screen = PartyScreen(
        session=session,
    )

    party_screen.party_size = Mock(
        return_value=3,
    )

    with pytest.raises(
        ValueError,
        match="Cannot select SLOT_6; party contains 3 Pokémon.",
    ):
        party_screen.select(
            PartySlot.SLOT_6,
        )

    session.press.assert_not_called()

def test_open_selected_opens_party_pokemon_menu(monkeypatch):
    session = Mock()

    party_screen = PartyScreen(
        session=session,
    )

    menu = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.party_screen.PartyPokemonMenu",
        Mock(return_value=menu),
    )

    result = party_screen.open_selected()

    session.press.assert_called_once_with(
        Button.A,
    )

    menu.wait_until_visible.assert_called_once_with()

    assert result is menu