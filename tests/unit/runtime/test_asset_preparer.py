import pytest

import bootstrap

from gameboy_automation.runtime.asset_preparer import AssetPreparer
from gameboy_automation.runtime.assets import Assets
from gameboy_automation.runtime.run_config import RunConfig
from gameboy_automation.runtime.workspace import Workspace


def test_prepare_copies_rom_and_save(tmp_path):
    source_rom = tmp_path / "source.gba"
    source_save = tmp_path / "source.sav"

    source_rom.write_bytes(b"rom-data")
    source_save.write_bytes(b"save-data")

    run_config = RunConfig(
        runtime_directory=tmp_path / "run_0001",
    )
    Workspace(run_config).create()

    assets = Assets(
        run_config=run_config,
        rom_filename="ultraviolet.gba",
        save_filename="ultraviolet.sav",
    )

    preparer = AssetPreparer(assets)

    preparer.prepare(
        source_rom=source_rom,
        source_save=source_save,
    )

    assert assets.rom_path.read_bytes() == b"rom-data"
    assert assets.save_path.read_bytes() == b"save-data"


def test_prepare_does_not_overwrite_existing_rom(tmp_path):
    source_rom = tmp_path / "source.gba"
    source_rom.write_bytes(b"new-rom-data")

    run_config = RunConfig(
        runtime_directory=tmp_path / "run_0001",
    )
    Workspace(run_config).create()

    assets = Assets(
        run_config=run_config,
        rom_filename="ultraviolet.gba",
        save_filename="ultraviolet.sav",
    )

    assets.rom_path.write_bytes(b"existing-rom-data")

    preparer = AssetPreparer(assets)

    with pytest.raises(FileExistsError):
        preparer.prepare(
            source_rom=source_rom,
        )

    assert assets.rom_path.read_bytes() == b"existing-rom-data"