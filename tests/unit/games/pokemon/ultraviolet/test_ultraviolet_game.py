from unittest.mock import Mock, patch

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.game import (
    UltraVioletGame,
)


def test_load_saved_game_navigates_to_quest_recap():
    session = Mock()

    title_screen = Mock()
    load_menu = Mock()
    quest_recap = Mock()

    game = UltraVioletGame(
        session=session,
    )

    with (
        patch(
            "gameboy_automation.games.pokemon.ultraviolet.game.TitleScreen",
            return_value=title_screen,
        ),
        patch(
            "gameboy_automation.games.pokemon.ultraviolet.game.LoadMenu",
            return_value=load_menu,
        ),
        patch(
            "gameboy_automation.games.pokemon.ultraviolet.game.QuestRecap",
            return_value=quest_recap,
        ),
    ):
        result = game.load_saved_game()

    title_screen.wait_until_visible.assert_called_once_with()
    title_screen.press_start.assert_called_once_with()

    load_menu.wait_until_visible.assert_called_once_with()
    load_menu.continue_game.assert_called_once_with()

    quest_recap.wait_until_visible.assert_called_once_with()

    assert result is quest_recap