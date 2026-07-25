import bootstrap
from pathlib import Path

from PIL import Image

from gameboy_automation.vision import Pixel, Screen


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

def test_screen_pixel() -> None:
    image = Image.new(
        mode="RGB",
        size=(10, 10),
    )

    image.putpixel(
        (3, 4),
        (10, 20, 30),
    )

    screen = Screen(image)

    pixel = screen.pixel(3, 4)

    assert pixel.red == 10
    assert pixel.green == 20
    assert pixel.blue == 30

def test_pixel_exact_match() -> None:
    a = Pixel(10, 20, 30)
    b = Pixel(10, 20, 30)

    assert a.is_close(b)


def test_pixel_with_tolerance() -> None:
    a = Pixel(100, 100, 100)
    b = Pixel(103, 98, 101)

    assert a.is_close(
        b,
        tolerance=3,
    )


def test_pixel_outside_tolerance() -> None:
    a = Pixel(100, 100, 100)
    b = Pixel(110, 100, 100)

    assert not a.is_close(
        b,
        tolerance=3,
    )

def test_pixel_matches() -> None:
    image = Image.new(
        mode="RGB",
        size=(10, 10),
    )

    image.putpixel(
        (5, 5),
        (100, 150, 200),
    )

    screen = Screen(image)

    assert screen.pixel_matches(
        5,
        5,
        Pixel(100, 150, 200),
    )

    assert screen.pixel_matches(
        5,
        5,
        Pixel(102, 149, 201),
        tolerance=2,
    )

    assert not screen.pixel_matches(
        5,
        5,
        Pixel(120, 150, 200),
        tolerance=2,
    )