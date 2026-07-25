from pathlib import Path
import sys
import time


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

from gameboy_automation.config import ProjectPaths  # noqa: E402
from gameboy_automation.emulators.mgba import MGBAEmulator  # noqa: E402
from gameboy_automation.vision import Screen  # noqa: E402


def test_mgba_screenshot() -> None:
    ProjectPaths.SCREENSHOTS.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        ProjectPaths.SCREENSHOTS
        / "test_mgba_screenshot.png"
    )

    emulator = MGBAEmulator(
        executable_path=ProjectPaths.MGBA_EXECUTABLE,
    )

    try:
        emulator.launch(
            ProjectPaths.ULTRAVIOLET_ROM,
        )

        print(f"Started mGBA ({emulator.pid})")

        emulator.wait_for_window()

        time.sleep(2)

        screen = emulator.screenshot()

        assert isinstance(screen, Screen)
        assert screen.width > 0
        assert screen.height > 0

        screen.save(output_file)

        assert output_file.exists()

        print(f"Screenshot size: {screen.size}")
        print(f"Screenshot saved to: {output_file}")

        time.sleep(3)

    finally:
        emulator.close()