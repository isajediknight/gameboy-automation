from unittest.mock import Mock

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.screens.quest_recap import (
    QUEST_RECAP_TEMPLATE_PATH,
    QuestRecap,
)
from gameboy_automation.emulators import Button

def test_is_visible_returns_true_when_template_is_found():
    match = Mock()
    match.found = True

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    quest_recap = QuestRecap(
        session=session,
    )

    assert quest_recap.is_visible() is True

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=QUEST_RECAP_TEMPLATE_PATH,
    )

def test_is_visible_returns_false_when_template_is_not_found():
    match = Mock()
    match.found = False

    screen = Mock()
    screen.find_template.return_value = match

    session = Mock()
    session.screenshot.return_value = screen

    quest_recap = QuestRecap(
        session=session,
    )

    assert quest_recap.is_visible() is False

    session.screenshot.assert_called_once_with()
    screen.find_template.assert_called_once_with(
        template_path=QUEST_RECAP_TEMPLATE_PATH,
    )

def test_wait_until_visible_waits_for_quest_recap(monkeypatch):
    quest_recap = QuestRecap(
        session=Mock(),
    )

    wait_until_mock = Mock()

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.quest_recap.wait_until",
        wait_until_mock,
    )

    quest_recap.wait_until_visible(
        timeout_seconds=5.0,
        poll_interval_seconds=0.25,
    )

    wait_until_mock.assert_called_once_with(
        quest_recap.is_visible,
        timeout_seconds=5.0,
        poll_interval_seconds=0.25,
        description="Pokémon Ultra Violet quest recap",
    )

def test_advance_presses_a_button():
    session = Mock()

    quest_recap = QuestRecap(
        session=session,
    )

    quest_recap.advance()

    session.press.assert_called_once_with(
        Button.A,
    )