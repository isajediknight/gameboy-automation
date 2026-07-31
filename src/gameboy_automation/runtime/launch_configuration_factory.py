from pathlib import Path

from gameboy_automation.emulators.base.config import LaunchConfiguration
from gameboy_automation.runtime.run_config import RunConfig


def create_launch_configuration(
    *,
    executable: Path,
    rom: Path,
    run_config: RunConfig,
) -> LaunchConfiguration:
    """
    Create launch configuration for a specific runtime workspace.
    """
    return LaunchConfiguration(
        executable=Path(executable),
        rom=Path(rom),
        working_directory=run_config.runtime_directory,
    )