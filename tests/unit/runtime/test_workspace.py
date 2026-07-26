import bootstrap

from gameboy_automation.runtime.run_config import RunConfig
from gameboy_automation.runtime.workspace import Workspace


def test_create_creates_runtime_directories(tmp_path):
    config = RunConfig(
        runtime_directory=tmp_path / "run_0001",
    )

    workspace = Workspace(config)

    workspace.create()

    assert config.runtime_directory.is_dir()
    assert config.roms_directory.is_dir()
    assert config.saves_directory.is_dir()
    assert config.states_directory.is_dir()
    assert config.screenshots_directory.is_dir()
    assert config.logs_directory.is_dir()
    assert config.temp_directory.is_dir()