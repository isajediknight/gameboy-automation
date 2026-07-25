from pathlib import Path

import bootstrap

from gameboy_automation.runtime.run_config import RunConfig


def test_directory_properties():
    config = RunConfig(Path("runtime/test/run_0001"))

    assert config.roms_directory == Path("runtime/test/run_0001/roms")
    assert config.saves_directory == Path("runtime/test/run_0001/saves")
    assert config.states_directory == Path("runtime/test/run_0001/states")
    assert config.screenshots_directory == Path("runtime/test/run_0001/screenshots")
    assert config.logs_directory == Path("runtime/test/run_0001/logs")
    assert config.temp_directory == Path("runtime/test/run_0001/temp")