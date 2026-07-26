from gameboy_automation.runtime.run_config import RunConfig


class Workspace:
    """
    Creates and manages the directories for one automation run.
    """

    def __init__(self, config: RunConfig) -> None:
        self.config = config

    def create(self) -> None:
        """
        Create the runtime directory and its standard subdirectories.

        Existing directories are left unchanged.
        """
        directories = (
            self.config.runtime_directory,
            self.config.roms_directory,
            self.config.saves_directory,
            self.config.states_directory,
            self.config.screenshots_directory,
            self.config.logs_directory,
            self.config.temp_directory,
        )

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )