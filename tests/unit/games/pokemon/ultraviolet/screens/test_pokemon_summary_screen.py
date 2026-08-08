from unittest.mock import Mock
import pytest
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

def test_level_reads_level_from_info_page(monkeypatch):
    session = Mock()
    screen = Mock()
    level_region = Mock()

    session.screenshot.return_value = screen

    screen.crop.return_value = level_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_info_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=28,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.level()

    assert result == 28

    screen.crop.assert_called_once_with(
        left=14,
        top=19,
        right=32,
        bottom=29,
    )

    read_number_auto_mock.assert_called_once_with(
        level_region,
    )

def test_level_requires_info_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_info_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon level can only be read from the Info page.",
    ):
        summary.level()

def test_current_hp_reads_hp_from_skills_page(monkeypatch):
    session = Mock()
    screen = Mock()
    hp_region = Mock()

    session.screenshot.return_value = screen
    screen.crop.return_value = hp_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_skills_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=233,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.current_hp()

    assert result == 233

    screen.crop.assert_called_once_with(
        left=195,
        top=20,
        right=213,
        bottom=30,
    )

    read_number_auto_mock.assert_called_once_with(
        hp_region,
    )

def test_current_hp_requires_skills_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_skills_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon current HP can only be read from the Skills page.",
    ):
        summary.current_hp()

def test_attack_reads_attack_from_skills_page(monkeypatch):
    session = Mock()
    screen = Mock()
    attack_region = Mock()

    session.screenshot.return_value = screen
    screen.crop.return_value = attack_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_skills_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=127,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.attack()

    assert result == 127

    screen.crop.assert_called_once_with(
        left=219,
        top=39,
        right=237,
        bottom=49,
    )

    read_number_auto_mock.assert_called_once_with(
        attack_region,
    )

def test_attack_requires_skills_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_skills_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon Attack can only be read from the Skills page.",
    ):
        summary.attack()

def test_defense_reads_defense_from_skills_page(monkeypatch):
    session = Mock()
    screen = Mock()
    defense_region = Mock()

    session.screenshot.return_value = screen
    screen.crop.return_value = defense_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_skills_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=101,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.defense()

    assert result == 101

    screen.crop.assert_called_once_with(
        left=219,
        top=51,
        right=237,
        bottom=61,
    )

    read_number_auto_mock.assert_called_once_with(
        defense_region,
    )

def test_defense_requires_skills_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_skills_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon Defense can only be read from the Skills page.",
    ):
        summary.defense()

def test_special_attack_reads_special_attack_from_skills_page(monkeypatch):
    session = Mock()
    screen = Mock()
    special_attack_region = Mock()

    session.screenshot.return_value = screen
    screen.crop.return_value = special_attack_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_skills_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=129,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.special_attack()

    assert result == 129

    screen.crop.assert_called_once_with(
        left=219,
        top=64,
        right=237,
        bottom=74,
    )

    read_number_auto_mock.assert_called_once_with(
        special_attack_region,
    )

def test_special_attack_requires_skills_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_skills_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon Special Attack can only be read from the Skills page.",
    ):
        summary.special_attack()

def test_special_defense_reads_special_defense_from_skills_page(monkeypatch):
    session = Mock()
    screen = Mock()
    special_defense_region = Mock()

    session.screenshot.return_value = screen
    screen.crop.return_value = special_defense_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_skills_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=132,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.special_defense()

    assert result == 132

    screen.crop.assert_called_once_with(
        left=219,
        top=77,
        right=237,
        bottom=87,
    )

    read_number_auto_mock.assert_called_once_with(
        special_defense_region,
    )

def test_special_defense_requires_skills_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_skills_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon Special Defense can only be read from the Skills page.",
    ):
        summary.special_defense()

def test_speed_reads_speed_from_skills_page(monkeypatch):
    session = Mock()
    screen = Mock()
    speed_region = Mock()

    session.screenshot.return_value = screen
    screen.crop.return_value = speed_region

    summary = PokemonSummaryScreen(
        session=session,
    )

    summary.is_skills_visible = Mock(
        return_value=True,
    )

    read_number_auto_mock = Mock(
        return_value=127,
    )

    monkeypatch.setattr(
        "gameboy_automation.games.pokemon.ultraviolet.screens.pokemon_summary_screen.read_number_auto",
        read_number_auto_mock,
    )

    result = summary.speed()

    assert result == 127

    screen.crop.assert_called_once_with(
        left=219,
        top=91,
        right=237,
        bottom=101,
    )

    read_number_auto_mock.assert_called_once_with(
        speed_region,
    )

def test_speed_requires_skills_page():
    summary = PokemonSummaryScreen(
        session=Mock(),
    )

    summary.is_skills_visible = Mock(
        return_value=False,
    )

    with pytest.raises(
        RuntimeError,
        match="Pokémon Speed can only be read from the Skills page.",
    ):
        summary.speed()