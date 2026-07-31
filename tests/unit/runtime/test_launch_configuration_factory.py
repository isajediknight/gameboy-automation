from pathlib import Path

import bootstrap

from gameboy_automation.runtime.launch_configuration_factory import (
    create_launch_configuration,
)
from gameboy_automation.runtime.run_config import RunConfig


def test_create_launch_configuration_uses_runtime_directory():
    run_config = RunConfig(
        runtime_directory=Path("runtime/test/run_0001"),
    )

    config = create_launch_configuration(
        executable=Path("emulators/mgba/executable/mGBA.exe"),
        rom=Path("roms/pokemon/ultraviolet/ultravioletv122.gba"),
        run_config=run_config,
    )

    assert config.executable == Path(
        "emulators/mgba/executable/mGBA.exe"
    )
    assert config.rom == Path(
        "roms/pokemon/ultraviolet/ultravioletv122.gba"
    )
    assert config.working_directory == Path(
        "runtime/test/run_0001"
    )