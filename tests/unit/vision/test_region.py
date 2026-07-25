import bootstrap
from pathlib import Path

from PIL import Image

from gameboy_automation.vision.screen import Pixel
from gameboy_automation.vision.screen import Screen


def test_region_has_expected_dimensions() -> None:
    screen = Screen(
        Image.new(
            mode="RGB",
            size=(20, 20),
            color=(255, 255, 255),
        )
    )

    region = screen.region(
        x=3,
        y=4,
        width=8,
        height=6,
    )

    assert region.image.size == (8, 6)


def test_region_pixel_uses_region_relative_coordinates() -> None:
    image = Image.new(
        mode="RGB",
        size=(20, 20),
        color=(255, 255, 255),
    )

    image.putpixel(
        (7, 9),
        (10, 20, 30),
    )

    screen = Screen(image)

    region = screen.region(
        x=5,
        y=6,
        width=10,
        height=10,
    )

    assert region.pixel(2, 3) == Pixel(
        red=10,
        green=20,
        blue=30,
    )


def test_region_save_writes_cropped_image(
    tmp_path: Path,
) -> None:
    image = Image.new(
        mode="RGB",
        size=(20, 20),
        color=(255, 255, 255),
    )

    image.putpixel(
        (4, 5),
        (10, 20, 30),
    )

    screen = Screen(image)

    region = screen.region(
        x=4,
        y=5,
        width=6,
        height=7,
    )

    output_path = tmp_path / "region.png"

    region.save(output_path)

    saved_image = Image.open(output_path)

    assert saved_image.size == (6, 7)
    assert saved_image.getpixel((0, 0)) == (10, 20, 30)


def test_region_find_template_uses_region_coordinates(
    tmp_path: Path,
) -> None:
    screen_image = Image.new(
        mode="RGB",
        size=(30, 30),
        color=(255, 255, 255),
    )

    template_image = Image.new(
        mode="RGB",
        size=(4, 4),
        color=(0, 0, 0),
    )

    template_image.putpixel((0, 0), (255, 0, 0))
    template_image.putpixel((3, 0), (0, 255, 0))
    template_image.putpixel((0, 3), (0, 0, 255))
    template_image.putpixel((3, 3), (255, 255, 0))

    screen_image.paste(
        template_image,
        (14, 17),
    )

    template_path = tmp_path / "template.png"
    template_image.save(template_path)

    screen = Screen(screen_image)

    region = screen.region(
        x=10,
        y=12,
        width=15,
        height=15,
    )

    match = region.find_template(
        template_path=template_path,
        confidence=0.99,
    )

    assert match.found is True
    assert match.x == 4
    assert match.y == 5
    assert match.width == 4
    assert match.height == 4