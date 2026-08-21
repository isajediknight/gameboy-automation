from unittest.mock import Mock
import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.egg_summary_screen import (
    EGG_SUMMARY_TEMPLATE_PATH,
    EggSummaryScreen,
)
from gameboy_automation.emulators import Button

def test_is_visible_returns_true_when_template_is_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = True

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    egg_summary = EggSummaryScreen(
        session=session,
    )

    assert egg_summary.is_visible() is True

    screen.find_template.assert_called_once_with(
        template_path=EGG_SUMMARY_TEMPLATE_PATH,
    )


def test_is_visible_returns_false_when_template_is_not_found():
    session = Mock()
    screen = Mock()
    match = Mock()

    match.found = False

    screen.find_template.return_value = match
    session.screenshot.return_value = screen

    egg_summary = EggSummaryScreen(
        session=session,
    )

    assert egg_summary.is_visible() is False

def test_close_returns_to_party_screen():
    session = Mock()

    egg_summary = EggSummaryScreen(
        session=session,
    )

    egg_summary.close()

    assert session.press.call_count == 2

    session.press.assert_called_with(
        Button.B,
    )