import bootstrap

from pathlib import Path
from unittest.mock import Mock

from gameboy_automation.emulators.base.config import EmulatorConfig
from gameboy_automation.emulators.mgba.adapter import MGBAEmulator


def test_launch_uses_rom_from_config_when_rom_is_not_provided(
    monkeypatch,
    tmp_path: Path,
) -> None:
    executable_path = tmp_path / "mgba.exe"
    rom_path = tmp_path / "pokemon.gba"

    executable_path.touch()
    rom_path.touch()

    config = EmulatorConfig(
        executable=executable_path,
        rom=rom_path,
    )

    popen_mock = Mock()
    process_mock = Mock()
    popen_mock.return_value = process_mock

    monkeypatch.setattr(
        "gameboy_automation.emulators.mgba.adapter.subprocess.Popen",
        popen_mock,
    )

    emulator = MGBAEmulator(
        executable_path=executable_path,
        config=config,
    )

    emulator.launch()

    resolved_rom_path = rom_path.resolve()

    assert emulator.rom_path == resolved_rom_path
    assert emulator.process is process_mock

    popen_mock.assert_called_once_with(
        [
            str(executable_path),
            str(resolved_rom_path),
        ],
        cwd=str(executable_path.parent),
    )