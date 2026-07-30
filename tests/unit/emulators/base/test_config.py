import bootstrap

from pathlib import Path

from gameboy_automation.emulators.base.config import LaunchConfiguration
def test_emulator_config_stores_required_paths() -> None:
    executable = Path("emulators/mgba/mgba.exe")
    rom = Path("roms/pokemon.gba")

    config = LaunchConfiguration(
        executable=executable,
        rom=rom,
    )

    assert config.executable == executable
    assert config.rom == rom


def test_emulator_config_working_directory_defaults_to_none() -> None:
    config = LaunchConfiguration(
        executable=Path("emulators/mgba/mgba.exe"),
        rom=Path("roms/pokemon.gba"),
    )

    assert config.working_directory is None


def test_emulator_config_stores_working_directory() -> None:
    working_directory = Path("emulators/mgba")

    config = LaunchConfiguration(
        executable=Path("emulators/mgba/mgba.exe"),
        rom=Path("roms/pokemon.gba"),
        working_directory=working_directory,
    )

    assert config.working_directory == working_directory