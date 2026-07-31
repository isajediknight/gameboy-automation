from pathlib import Path
from unittest.mock import Mock

import bootstrap

from gameboy_automation.emulators.base.config import LaunchConfiguration
from gameboy_automation.runtime.assets import Assets
from gameboy_automation.runtime.run_config import RunConfig
from gameboy_automation.runtime.session import Session
from gameboy_automation.runtime.source_assets import SourceAssets
from gameboy_automation.runtime.workspace import Workspace
from gameboy_automation.emulators.mgba.adapter import MGBAEmulator
from gameboy_automation.emulators.base import Button


def test_session_stores_components():
    run_config = RunConfig(
        runtime_directory=Path("runtime/test/run_0001"),
    )

    source_assets = SourceAssets(
        rom=Path("roms/pokemon/ultraviolet.gba"),
        save=Path("saves/luke.sav"),
    )

    workspace = Workspace(run_config)

    assets = Assets(
        run_config=run_config,
        rom_filename="ultraviolet.gba",
        save_filename="ultraviolet.sav",
    )

    launch_configuration = LaunchConfiguration(
        executable=Path("mGBA.exe"),
        rom=assets.rom_path,
        working_directory=run_config.runtime_directory,
    )

    emulator = MGBAEmulator(
        executable_path=launch_configuration.executable,
        config=launch_configuration,
    )

    session = Session(
        run_config=run_config,
        source_assets=source_assets,
        workspace=workspace,
        assets=assets,
        launch_configuration=launch_configuration,
        emulator=emulator,
    )

    assert session.run_config is run_config
    assert session.source_assets is source_assets
    assert session.workspace is workspace
    assert session.assets is assets
    assert session.launch_configuration is launch_configuration


def test_prepare_creates_workspace_and_copies_assets(tmp_path):
    source_rom = tmp_path / "source.gba"
    source_rom.write_bytes(b"rom-data")

    run_config = RunConfig(
        runtime_directory=tmp_path / "run_0001",
    )

    source_assets = SourceAssets(
        rom=source_rom,
    )

    workspace = Workspace(run_config)

    assets = Assets(
        run_config=run_config,
        rom_filename="ultraviolet.gba",
        save_filename="ultraviolet.sav",
    )

    launch_configuration = LaunchConfiguration(
        executable=Path("mGBA.exe"),
        rom=assets.rom_path,
        working_directory=run_config.runtime_directory,
    )

    emulator = MGBAEmulator(
        executable_path=launch_configuration.executable,
        config=launch_configuration,
    )

    session = Session(
        run_config=run_config,
        source_assets=source_assets,
        workspace=workspace,
        assets=assets,
        launch_configuration=launch_configuration,
        emulator=emulator,
    )

    session.prepare()

    assert run_config.runtime_directory.is_dir()
    assert run_config.roms_directory.is_dir()
    assert run_config.saves_directory.is_dir()
    assert run_config.states_directory.is_dir()
    assert run_config.screenshots_directory.is_dir()
    assert run_config.logs_directory.is_dir()
    assert run_config.temp_directory.is_dir()
    assert assets.rom_path.read_bytes() == b"rom-data"

def test_launch_delegates_to_emulator():
    emulator = Mock()

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    session.launch()

    emulator.launch.assert_called_once_with()

def test_stop_delegates_to_emulator():
    emulator = Mock()

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    session.stop()

    emulator.close.assert_called_once_with()

def test_screenshot_delegates_to_emulator():
    expected_screen = Mock()

    emulator = Mock()
    emulator.screenshot.return_value = expected_screen

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    screen = session.screenshot()

    emulator.screenshot.assert_called_once_with()
    assert screen is expected_screen

def test_press_delegates_to_emulator():
    emulator = Mock()

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    session.press(Button.A)

    emulator.press.assert_called_once_with(
        Button.A,
        duration_seconds=0.1,
    )

def test_press_passes_custom_duration():
    emulator = Mock()

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    session.press(
        Button.START,
        duration_seconds=0.25,
    )

    emulator.press.assert_called_once_with(
        Button.START,
        duration_seconds=0.25,
    )

def test_key_down_delegates_to_emulator():
    emulator = Mock()

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    session.key_down(Button.A)

    emulator.key_down.assert_called_once_with(Button.A)


def test_key_up_delegates_to_emulator():
    emulator = Mock()

    session = Session(
        run_config=Mock(),
        source_assets=Mock(),
        workspace=Mock(),
        assets=Mock(),
        launch_configuration=Mock(),
        emulator=emulator,
    )

    session.key_up(Button.A)

    emulator.key_up.assert_called_once_with(Button.A)