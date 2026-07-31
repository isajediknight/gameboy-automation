from dataclasses import dataclass

from gameboy_automation.emulators.base.config import LaunchConfiguration
from gameboy_automation.runtime.assets import Assets
from gameboy_automation.runtime.run_config import RunConfig
from gameboy_automation.runtime.workspace import Workspace
from gameboy_automation.runtime.source_assets import SourceAssets
from gameboy_automation.runtime.asset_preparer import AssetPreparer
from gameboy_automation.vision import Screen
from gameboy_automation.emulators.base import (
    Button,
    Emulator,
)


@dataclass(frozen=True)
class Session:
    """
    Represents one emulator automation session.

    At this stage, Session simply groups together the
    objects required to execute a run.
    """

    run_config: RunConfig
    source_assets: SourceAssets
    workspace: Workspace
    assets: Assets
    launch_configuration: LaunchConfiguration
    emulator: Emulator
    
    def prepare(self) -> None:
        """
        Prepare the runtime workspace and emulator assets.
        """
        self.workspace.create()

        self._asset_preparer().prepare(
            source_rom=self.source_assets.rom,
            source_save=self.source_assets.save,
        )

    def launch(self) -> None:
        """
        Launch the emulator.
        """
        self.emulator.launch()

    def stop(self) -> None:
        """
        Stop the emulator.
        """
        self.emulator.close()

    def screenshot(self) -> Screen:
        """
        Capture the current emulator screen.
        """
        return self.emulator.screenshot()

    def _asset_preparer(self) -> AssetPreparer:
        """
        Create an AssetPreparer for this session.
        """
        return AssetPreparer(self.assets)

    def press(
        self,
        button: Button,
        duration_seconds: float = 0.1,
    ) -> None:
        """
        Press and release an emulator button.
        """
        self.emulator.press(
            button,
            duration_seconds=duration_seconds,
        )

    def key_down(self, button: Button) -> None:
        """
        Press and hold an emulator button.
        """
        self.emulator.key_down(button)


    def key_up(self, button: Button) -> None:
        """
        Release an emulator button.
        """
        self.emulator.key_up(button)