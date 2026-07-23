import bootstrap
from pathlib import Path

from PIL import Image

from gameboy_automation.vision import Screen


def test_screen_dimensions() -> None:
    image = Image.new(
        mode="RGB",
        size=(240, 160),
    )

    screen = Screen(image)

    assert screen.width == 240
    assert screen.height == 160
    assert screen.size == (240, 160)


def test_screen_crop() -> None:
    image = Image.new(
        mode="RGB",
        size=(240, 160),
    )

    screen = Screen(image)

    cropped_screen = screen.crop(
        left=10,
        top=20,
        right=110,
        bottom=70,
    )

    assert cropped_screen.size == (100, 50)


def test_screen_save(tmp_path: Path) -> None:
    image = Image.new(
        mode="RGB",
        size=(240, 160),
    )

    screen = Screen(image)

    output_path = tmp_path / "screenshots" / "screen.png"

    screen.save(output_path)

    assert output_path.exists()