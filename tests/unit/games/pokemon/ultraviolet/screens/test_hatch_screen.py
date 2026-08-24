from unittest.mock import Mock

from gameboy_automation.games.pokemon.ultraviolet.screens.hatch_screen import (
    HATCH_HUH_TEMPLATE_PATH,
    HatchScreen,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.hatch_screen import (
    HATCH_HATCHED_TEMPLATE_PATH,
    HATCH_HUH_TEMPLATE_PATH,
    HATCH_NICKNAME_TEMPLATE_PATH,
    HatchScreen,
)

def test_is_visible_returns_true_when_hatch_screen_is_visible():
    session = Mock()

    screen = session.screenshot.return_value
    match = screen.find_template.return_value
    match.found = True

    hatch_screen = HatchScreen(
        session=session,
    )

    result = hatch_screen.is_visible()

    assert result is True

    session.screenshot.assert_called_once_with()

    screen.find_template.assert_called_once_with(
        template_path=HATCH_HUH_TEMPLATE_PATH,
    )


def test_is_visible_returns_false_when_hatch_screen_is_not_visible():
    session = Mock()

    screen = session.screenshot.return_value
    match = screen.find_template.return_value
    match.found = False

    hatch_screen = HatchScreen(
        session=session,
    )

    result = hatch_screen.is_visible()

    assert result is False

def test_is_hatched_visible_returns_true_when_hatch_complete_dialogue_is_visible():
    session = Mock()

    screen = session.screenshot.return_value
    match = screen.find_template.return_value
    match.found = True

    hatch_screen = HatchScreen(
        session=session,
    )

    result = hatch_screen.is_hatched_visible()

    assert result is True

    session.screenshot.assert_called_once_with()

    screen.find_template.assert_called_once_with(
        template_path=HATCH_HATCHED_TEMPLATE_PATH,
    )


def test_is_nickname_visible_returns_true_when_nickname_prompt_is_visible():
    session = Mock()

    screen = session.screenshot.return_value
    match = screen.find_template.return_value
    match.found = True

    hatch_screen = HatchScreen(
        session=session,
    )

    result = hatch_screen.is_nickname_visible()

    assert result is True

    session.screenshot.assert_called_once_with()

    screen.find_template.assert_called_once_with(
        template_path=HATCH_NICKNAME_TEMPLATE_PATH,
    )