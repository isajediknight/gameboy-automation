from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    """
    Configuration describing a single automation run.
    """

    runtime_directory: Path

    @property
    def roms_directory(self) -> Path:
        return self.runtime_directory / "roms"

    @property
    def saves_directory(self) -> Path:
        return self.runtime_directory / "saves"

    @property
    def states_directory(self) -> Path:
        return self.runtime_directory / "states"

    @property
    def screenshots_directory(self) -> Path:
        return self.runtime_directory / "screenshots"

    @property
    def logs_directory(self) -> Path:
        return self.runtime_directory / "logs"

    @property
    def temp_directory(self) -> Path:
        return self.runtime_directory / "temp"