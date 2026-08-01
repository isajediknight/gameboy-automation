from pathlib import Path
import subprocess
import time

from PIL import Image

from gameboy_automation.emulators.base import (
    Button,
    Emulator,
)
from gameboy_automation.emulators.mgba.keys import (
    BUTTON_TO_VIRTUAL_KEY,
)
from gameboy_automation.utils.windows import (
    capture_client_area,
    find_window_by_process_id,
    send_key_down,
    send_key_up,
)

from gameboy_automation.vision import Screen
from gameboy_automation.emulators.base.config import LaunchConfiguration
from gameboy_automation.emulators.mgba.screenshots import (
    extract_game_viewport,
)

class MGBAEmulator(Emulator):
    """mGBA emulator process adapter."""

    def __init__(
        self,
        executable_path: Path,
        config: LaunchConfiguration | None = None,
    ) -> None:
        super().__init__(
            executable_path=executable_path,
            config=config,
        )

        self._window_handle: int | None = None

    @property
    def window_handle(self) -> int | None:
        """Return the cached native mGBA window handle."""
        return self._window_handle

    def launch(self, rom_path: Path | None = None) -> None:
        """
        Launch mGBA, optionally opening a ROM.

        Args:
            rom_path:
                Optional path to a Game Boy Advance ROM.
        """
        if self.is_running():
            raise RuntimeError("mGBA is already running.")

        effective_rom_path = rom_path

        if effective_rom_path is None and self.config is not None:
            effective_rom_path = self.config.rom

        if not self.executable_path.is_file():
            raise FileNotFoundError(
                f"mGBA executable not found: {self.executable_path}"
            )

        command = [str(self.executable_path)]

        self.rom_path = None
        self._window_handle = None

        if effective_rom_path is not None:
            resolved_rom_path = Path(effective_rom_path).resolve()

            if not resolved_rom_path.is_file():
                raise FileNotFoundError(
                    f"ROM file not found: {resolved_rom_path}"
                )

            self.rom_path = resolved_rom_path
            command.append(str(resolved_rom_path))

        try:
            self.process = subprocess.Popen(
                command,
                cwd=str(self.executable_path.parent),
            )
        except OSError:
            self.process = None
            self.rom_path = None
            self._window_handle = None
            raise

    def wait_for_window(
        self,
        timeout_seconds: float = 10.0,
        poll_interval_seconds: float = 0.1,
    ) -> int:
        """
        Wait until the visible mGBA window is available.

        Args:
            timeout_seconds:
                Maximum time to wait for the mGBA window.
            poll_interval_seconds:
                Delay between window-discovery attempts.

        Returns:
            The native Windows window handle.

        Raises:
            RuntimeError:
                If mGBA is not running.
            TimeoutError:
                If the window is not found before the timeout.
        """
        if not self.is_running():
            raise RuntimeError("mGBA is not running.")

        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            assert self.pid is not None

            window_handle = find_window_by_process_id(
                self.pid,
            )

            if window_handle is not None:
                self._window_handle = window_handle
                return window_handle

            time.sleep(poll_interval_seconds)

        raise TimeoutError(
            f"mGBA window was not found within "
            f"{timeout_seconds:.1f} seconds."
        )


    def screenshot(self) -> Screen:
        """
        Capture the current emulator display.

        Returns:
            A Screen object containing the current emulator image.
        """
        if self._window_handle is None:
            raise RuntimeError(
                "The emulator window has not been located."
            )

        image = capture_client_area(self._window_handle)
        game_viewport = extract_game_viewport(image)

        screen = Screen(game_viewport)

        return screen.resize(
            width=240,
            height=160,
        )

    def close(self, timeout_seconds: float = 10.0) -> None:
        """Close mGBA and clear cached window state."""
        try:
            super().close(timeout_seconds=timeout_seconds)
        finally:
            self._window_handle = None

    def kill(self) -> None:
        """Forcefully stop mGBA and clear cached window state."""
        try:
            super().kill()
        finally:
            self._window_handle = None
    
    def key_down(self, button: Button) -> None:
        """
        Press and hold an emulator button.

        Args:
            button:
                Game Boy Advance button to hold.
        """
        if not self.is_running():
            raise RuntimeError("mGBA is not running.")

        if self._window_handle is None:
            self.wait_for_window()

        assert self._window_handle is not None

        try:
            virtual_key_code = BUTTON_TO_VIRTUAL_KEY[button]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported mGBA button: {button!r}"
            ) from exc

        send_key_down(
            self._window_handle,
            virtual_key_code,
        )

    def key_up(self, button: Button) -> None:
        """
        Release an emulator button.

        Args:
            button:
                Game Boy Advance button to release.
        """
        if not self.is_running():
            raise RuntimeError("mGBA is not running.")

        if self._window_handle is None:
            self.wait_for_window()

        assert self._window_handle is not None

        try:
            virtual_key_code = BUTTON_TO_VIRTUAL_KEY[button]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported mGBA button: {button!r}"
            ) from exc

        send_key_up(
            self._window_handle,
            virtual_key_code,
        )


