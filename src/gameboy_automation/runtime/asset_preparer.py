from pathlib import Path
from shutil import copy2

from gameboy_automation.runtime.assets import Assets


class AssetPreparer:
    """
    Copies source emulator assets into a runtime workspace.
    """

    def __init__(self, assets: Assets) -> None:
        self.assets = assets

    def prepare(
        self,
        *,
        source_rom: Path,
        source_save: Path | None = None,
    ) -> None:
        """
        Copy the source ROM and optional save into the runtime workspace.

        Existing destination files are not overwritten.
        """
        source_rom = Path(source_rom)

        if not source_rom.is_file():
            raise FileNotFoundError(source_rom)

        if self.assets.rom_path.exists():
            raise FileExistsError(self.assets.rom_path)

        source_save_path: Path | None = None

        if source_save is not None:
            source_save_path = Path(source_save)

            if not source_save_path.is_file():
                raise FileNotFoundError(source_save_path)

            if self.assets.save_path.exists():
                raise FileExistsError(self.assets.save_path)

        copy2(
            source_rom,
            self.assets.rom_path,
        )

        if source_save_path is not None:
            copy2(
                source_save_path,
                self.assets.save_path,
            )