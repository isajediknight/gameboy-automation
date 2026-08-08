from unittest.mock import Mock

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen import (
    POKEMON_SUMMARY_INFO_TEMPLATE_PATH,
    POKEMON_SUMMARY_MOVES_TEMPLATE_PATH,
    POKEMON_SUMMARY_SKILLS_TEMPLATE_PATH,
    PokemonSummaryScreen,
    PokemonSummaryPage,
)
from gameboy_automation.emulators import Button

def test_is_info_visible_returns_true_when_template_is_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    assert summary.is_info_visible() is True

    screen.find_template.assert_called_once_with(
        template_path=POKEMON_SUMMARY_INFO_TEMPLATE_PATH,
    )


def test_is_info_visible_returns_false_when_template_is_not_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = False

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    assert summary.is_info_visible() is False


def test_wait_until_info_visible_returns_when_info_page_is_visible():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.wait_until_info_visible(
        timeout_seconds=0.1,
        poll_interval_seconds=0.01,
    )

def test_is_skills_visible_returns_true_when_template_is_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    assert summary.is_skills_visible() is True

    screen.find_template.assert_called_once_with(
        template_path=POKEMON_SUMMARY_SKILLS_TEMPLATE_PATH,
    )


def test_wait_until_skills_visible_returns_when_skills_page_is_visible():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.wait_until_skills_visible(
        timeout_seconds=0.1,
        poll_interval_seconds=0.01,
    )


def test_is_moves_visible_returns_true_when_template_is_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    assert summary.is_moves_visible() is True

    screen.find_template.assert_called_once_with(
        template_path=POKEMON_SUMMARY_MOVES_TEMPLATE_PATH,
    )


def test_wait_until_moves_visible_returns_when_moves_page_is_visible():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.wait_until_moves_visible(
        timeout_seconds=0.1,
        poll_interval_seconds=0.01,
    )

def test_current_page_returns_info():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_info_visible = Mock(
        return_value=True,
    )

    assert summary.current_page() is PokemonSummaryPage.INFO


def test_go_to_moves_from_info_to_moves(monkeypatch):
    session = Mock()

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.current_page = Mock(
        return_value=PokemonSummaryPage.INFO,
    )

    summary.wait_until_skills_visible = Mock()
    summary.wait_until_moves_visible = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.time.sleep",
        Mock(),
    )

    summary.go_to(
        PokemonSummaryPage.MOVES,
    )

    assert session.press.call_count == 2

    session.press.assert_called_with(
        Button.RIGHT,
        duration_seconds=0.5,
    )

    summary.wait_until_skills_visible.assert_called_once_with()
    summary.wait_until_moves_visible.assert_called_once_with()


def test_go_to_moves_from_moves_to_info():
    session = Mock()

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.current_page = Mock(
        return_value=PokemonSummaryPage.MOVES,
    )

    summary.wait_until_skills_visible = Mock()
    summary.wait_until_info_visible = Mock()

    summary.go_to(
        PokemonSummaryPage.INFO,
    )

    assert session.press.call_count == 2

    session.press.assert_called_with(
        Button.LEFT,
        duration_seconds=0.5,
    )

    summary.wait_until_skills_visible.assert_called_once_with()
    summary.wait_until_info_visible.assert_called_once_with()