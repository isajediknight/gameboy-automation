from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceAssets:
    """
    Original files used to prepare an emulator session.
    """

    rom: Path
    save: Path | None = None