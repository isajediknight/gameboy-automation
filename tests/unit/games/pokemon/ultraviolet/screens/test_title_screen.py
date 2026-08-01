from unittest.mock import Mock

import bootstrap
import pytest

from gameboy_automation.games.pokemon.ultraviolet.screens.title_screen import (
    TITLE_SCREEN_TEMPLATE_PATH,
    TitleScreen,
)
from gameboy_automation.services.wait import WaitTimeoutError
from gameboy_automation.emulators import Button

def test_is_visible_returns_true_when_template_is_found():
    match = Mock()
    match.found = True

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    title_screen = TitleScreen(
        session=session,
    )

    assert title_screen.is_visible() is True

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=TITLE_SCREEN_TEMPLATE_PATH,
    )


def test_is_visible_returns_false_when_template_is_not_found():
    match = Mock()
    match.found = False

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    title_screen = TitleScreen(
        session=session,
    )

    assert title_screen.is_visible() is False

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=TITLE_SCREEN_TEMPLATE_PATH,
    )


def test_wait_until_visible_returns_when_title_screen_is_visible():
    match = Mock()
    match.found = True

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    title_screen = TitleScreen(
        session=session,
    )

    title_screen.wait_until_visible(
        timeout_seconds=1.0,
        poll_interval_seconds=0.0,
    )

    session.screenshot.assert_called_once_with()


def test_wait_until_visible_times_out_when_title_screen_is_not_visible():
    match = Mock()
    match.found = False

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    title_screen = TitleScreen(
        session=session,
    )

    with pytest.raises(WaitTimeoutError):
        title_screen.wait_until_visible(
            timeout_seconds=0.01,
            poll_interval_seconds=0.0,
        )

def test_press_start_presses_start_button():
    session = Mock()

    title_screen = TitleScreen(
        session=session,
    )

    title_screen.press_start()

    session.press.assert_called_once_with(
        Button.START,
    )