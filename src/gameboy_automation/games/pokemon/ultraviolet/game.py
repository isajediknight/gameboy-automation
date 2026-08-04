import time

from gameboy_automation.games.pokemon.ultraviolet.screens.load_menu import (
    LoadMenu,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.quest_recap import (
    QuestRecap,
)
from gameboy_automation.games.pokemon.ultraviolet.screens.title_screen import (
    TitleScreen,
)
from gameboy_automation.runtime.session import Session


class UltraVioletGame:
    """High-level automation for Pokémon Ultra Violet."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def load_saved_game(self) -> None:
        """
        Navigate from the title screen into the loaded saved game.
        """
        title_screen = TitleScreen(
            session=self.session,
        )

        title_screen.wait_until_visible()
        title_screen.press_start()

        load_menu = LoadMenu(
            session=self.session,
        )

        load_menu.wait_until_visible()

        time.sleep(1)

        load_menu.continue_game()

        quest_recap = QuestRecap(
            session=self.session,
        )

        quest_recap.wait_until_visible()
        quest_recap.skip()