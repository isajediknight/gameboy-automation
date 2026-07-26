from dataclasses import dataclass
from pathlib import Path

from gameboy_automation.runtime.run_config import RunConfig


@dataclass(frozen=True)
class Assets:
    """
    File and directory locations used by one emulator run.
    """

    run_config: RunConfig
    rom_filename: str
    save_filename: str

    @property
    def rom_path(self) -> Path:
        return self.run_config.roms_directory / self.rom_filename

    @property
    def save_path(self) -> Path:
        return self.run_config.saves_directory / self.save_filename

    @property
    def quicksave_directory(self) -> Path:
        return self.run_config.states_directory

    @property
    def screenshots_directory(self) -> Path:
        return self.run_config.screenshots_directory