from pathlib import Path

import bootstrap

from gameboy_automation.runtime.assets import Assets
from gameboy_automation.runtime.run_config import RunConfig


def test_runtime_asset_paths():
    run_config = RunConfig(
        runtime_directory=Path("runtime/test/run_0001"),
    )

    assets = Assets(
        run_config=run_config,
        rom_filename="ultraviolet.gba",
        save_filename="ultraviolet.sav",
    )

    assert assets.rom_path == Path(
        "runtime/test/run_0001/roms/ultraviolet.gba"
    )
    assert assets.save_path == Path(
        "runtime/test/run_0001/saves/ultraviolet.sav"
    )
    assert assets.quicksave_directory == Path(
        "runtime/test/run_0001/states"
    )
    assert assets.screenshots_directory == Path(
        "runtime/test/run_0001/screenshots"
    )