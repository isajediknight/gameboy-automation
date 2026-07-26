from pathlib import Path

from gameboy_automation.emulators.base.config import EmulatorConfig
from gameboy_automation.runtime.run_config import RunConfig


def create_emulator_config(
    *,
    executable: Path,
    rom: Path,
    run_config: RunConfig,
) -> EmulatorConfig:
    """
    Create emulator configuration for a specific runtime workspace.
    """
    return EmulatorConfig(
        executable=Path(executable),
        rom=Path(rom),
        working_directory=run_config.runtime_directory,
    )