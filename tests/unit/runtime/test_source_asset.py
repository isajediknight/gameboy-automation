from pathlib import Path

import bootstrap

from gameboy_automation.runtime.source_assets import SourceAssets


def test_source_assets_stores_rom_and_save_paths():
    source_assets = SourceAssets(
        rom=Path("roms/pokemon/ultraviolet.gba"),
        save=Path("saves/luke.sav"),
    )

    assert source_assets.rom == Path(
        "roms/pokemon/ultraviolet.gba"
    )
    assert source_assets.save == Path(
        "saves/luke.sav"
    )


def test_source_assets_allows_missing_save():
    source_assets = SourceAssets(
        rom=Path("roms/pokemon/ultraviolet.gba"),
    )

    assert source_assets.rom == Path(
        "roms/pokemon/ultraviolet.gba"
    )
    assert source_assets.save is None