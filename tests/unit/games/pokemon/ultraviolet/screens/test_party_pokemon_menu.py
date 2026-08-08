import bootstrap
from unittest.mock import Mock

from gameboy_automation.games.pokemon.ultraviolet.screens.party_pokemon_menu import (
    PARTY_POKEMON_MENU_TEMPLATE_PATH,
    PartyPokemonMenu,
)
from gameboy_automation.emulators import Button

def test_is_visible_returns_true_when_template_is_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    menu = PartyPokemonMenu(
        session=session,
    )

    assert menu.is_visible() is True

    screen.find_template.assert_called_once_with(
        template_path=PARTY_POKEMON_MENU_TEMPLATE_PATH,
    )


def test_is_visible_returns_false_when_template_is_not_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = False

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    menu = PartyPokemonMenu(
        session=session,
    )

    assert menu.is_visible() is False


def test_wait_until_visible_returns_when_menu_is_visible():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    menu = PartyPokemonMenu(
        session=session,
    )

    menu.wait_until_visible(
        timeout_seconds=0.1,
        poll_interval_seconds=0.01,
    )

def test_confirm_presses_a_button():
    session = Mock()

    menu = PartyPokemonMenu(
        session=session,
    )

    menu.confirm()

    session.press.assert_called_once_with(
        Button.A,
    )