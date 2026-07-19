from pathlib import Path
import subprocess

from gameboy_automation.emulators.base import Emulator


class MGBAEmulator(Emulator):
    """mGBA emulator process adapter."""

    def launch(self, rom_path: Path | None = None) -> None:
        """
        Launch mGBA, optionally opening a ROM.

        Args:
            rom_path:
                Optional path to a Game Boy Advance ROM.
        """
        if self.is_running():
            raise RuntimeError("mGBA is already running.")

        if not self.executable_path.is_file():
            raise FileNotFoundError(
                f"mGBA executable not found: {self.executable_path}"
            )

        command = [str(self.executable_path)]

        self.rom_path = None

        if rom_path is not None:
            resolved_rom_path = Path(rom_path).resolve()

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
            raise