from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import Popen, TimeoutExpired
from typing import Optional
import subprocess
import time
from gameboy_automation.vision import Screen

from .button import Button

class Emulator(ABC):
    """Base interface for supported Game Boy emulators."""

    def __init__(self, executable_path: Path) -> None:
        self.executable_path = Path(executable_path)
        self.process: Optional[Popen] = None
        self.rom_path: Optional[Path] = None

    @abstractmethod
    def launch(self, rom_path: Path | None = None) -> None:
        """
        Launch the emulator.

        Args:
            rom_path:
                Optional path to the ROM that should be opened.
        """

    @abstractmethod
    def screenshot(self) -> Screen:
        """
        Capture the current emulator screen.

        Returns:
            A Screen object representing the current display.
        """
        raise NotImplementedError

    @abstractmethod
    def key_down(self, button: Button) -> None:
        """Press and hold an emulator button."""
        raise NotImplementedError

    @abstractmethod
    def key_up(self, button: Button) -> None:
        """Release an emulator button."""
        raise NotImplementedError

    def is_running(self) -> bool:
        """Return True when the emulator process is running."""
        return self.process is not None and self.process.poll() is None

    @property
    def pid(self) -> int | None:
        """Return the emulator process ID while it is running."""
        if not self.is_running():
            return None

        assert self.process is not None
        return self.process.pid

    def press(
        self,
        button: Button,
        duration_seconds: float = 0.1,
    ) -> None:
        """
        Press and release an emulator button.

        Args:
            button:
                Button to press.
            duration_seconds:
                How long to hold the button before releasing it.
        """
        if duration_seconds < 0:
            raise ValueError(
                "duration_seconds cannot be negative."
            )

        self.key_down(button)

        try:
            time.sleep(duration_seconds)
        finally:
            self.key_up(button)

    def hold(
        self,
        button: Button,
        duration_seconds: float,
    ) -> None:
        """
        Hold an emulator button for a fixed duration.

        Args:
            button:
                Button to hold.
            duration_seconds:
                How long to hold the button.
        """
        self.press(
            button,
            duration_seconds=duration_seconds,
        )

    def close(self, timeout_seconds: float = 10.0) -> None:
        """
        Request that the emulator process terminate.

        If the process does not terminate before the timeout, it is
        forcefully killed.
        """
        if not self.is_running():
            self.process = None
            return

        assert self.process is not None

        self.process.terminate()

        try:
            self.process.wait(timeout=timeout_seconds)
        except TimeoutExpired:
            self.process.kill()
            self.process.wait()

        self.process = None

    def kill(self) -> None:
        """Forcefully stop the emulator process."""
        if not self.is_running():
            self.process = None
            return

        assert self.process is not None

        self.process.kill()
        self.process.wait()
        self.process = None

    def wait_until_closed(self, timeout_seconds: float | None = None) -> int:
        """
        Wait for the emulator process to exit.

        Returns:
            The process exit code.

        Raises:
            RuntimeError:
                If the emulator has not been launched.
            subprocess.TimeoutExpired:
                If a timeout is provided and the process remains open.
        """
        if self.process is None:
            raise RuntimeError("The emulator has not been launched.")

        exit_code = self.process.wait(timeout=timeout_seconds)
        self.process = None

        return exit_code

    def __enter__(self) -> "Emulator":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()