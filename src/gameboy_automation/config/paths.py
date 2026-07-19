from pathlib import Path


class ProjectPaths:
    """Centralized paths for the gameboy-automation repository."""

    REPO_ROOT = Path(__file__).resolve().parents[3]

    SRC = REPO_ROOT / "src"
    TESTS = REPO_ROOT / "tests"

    EMULATORS = REPO_ROOT / "emulators"

    MGBA = EMULATORS / "mgba"
    MGBA_EXECUTABLE_DIRECTORY = MGBA / "executable"
    MGBA_EXECUTABLE = MGBA_EXECUTABLE_DIRECTORY / "mGBA.exe"

    ROMS = REPO_ROOT / "roms"

    POKEMON_ROMS = ROMS / "pokemon"

    ULTRAVIOLET = POKEMON_ROMS / "ultraviolet"
    ULTRAVIOLET_ROM = ULTRAVIOLET / "ultravioletv122.gba"

    OUTPUT = REPO_ROOT / "output"

    SCREENSHOTS = OUTPUT / "screenshots"