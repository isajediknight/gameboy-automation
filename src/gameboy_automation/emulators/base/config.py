from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LaunchConfiguration:
    """
    Filesystem configuration required to launch an emulator.
    """

    executable: Path
    rom: Path
    working_directory: Path | None = None