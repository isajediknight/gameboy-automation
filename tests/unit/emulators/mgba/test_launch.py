import bootstrap

from PIL import Image

from gameboy_automation.vision.screen import Screen
from pathlib import Path
from unittest.mock import Mock, patch

from gameboy_automation.emulators.base.config import LaunchConfiguration
from gameboy_automation.emulators.mgba.adapter import MGBAEmulator


def test_launch_uses_rom_from_config_when_rom_is_not_provided(
    monkeypatch,
    tmp_path: Path,
) -> None:
    executable_path = tmp_path / "mgba.exe"
    rom_path = tmp_path / "pokemon.gba"

    executable_path.touch()
    rom_path.touch()

    config = LaunchConfiguration(
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

def test_screenshot_extracts_game_viewport():
    client_image = Image.new(
        mode="RGB",
        size=(480, 340),
    )

    viewport_image = Image.new(
        mode="RGB",
        size=(480, 320),
    )

    emulator = MGBAEmulator(
        executable_path=Path("mgba.exe"),
    )

    emulator._window_handle = 123

    with (
        patch(
            "gameboy_automation.emulators.mgba.adapter.capture_client_area",
            return_value=client_image,
        ) as capture_mock,
        patch(
            "gameboy_automation.emulators.mgba.adapter.extract_game_viewport",
            return_value=viewport_image,
        ) as extract_mock,
    ):
        screen = emulator.screenshot()

    assert isinstance(screen, Screen)
    assert screen.size == (240, 160)

    capture_mock.assert_called_once_with(123)
    extract_mock.assert_called_once_with(client_image)