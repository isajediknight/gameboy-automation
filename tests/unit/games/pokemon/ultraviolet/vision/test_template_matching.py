from pathlib import Path

from PIL import Image

import bootstrap

from gameboy_automation.vision import Screen
from gameboy_automation.vision.template_matching import (
    find_screen_in_reference,
)

def test_find_screen_in_reference_finds_exact_region(
    tmp_path: Path,
):
    reference = Image.new(
        "RGB",
        (100, 80),
        "black",
    )

    for x in range(30, 50):
        for y in range(20, 40):
            reference.putpixel(
                (x, y),
                (255, 255, 255),
            )

    reference_path = (
        tmp_path
        / "reference.png"
    )

    reference.save(
        reference_path,
    )

    screen_image = reference.crop(
        (
            20,
            10,
            70,
            60,
        )
    )

    screen = Screen(
        screen_image,
    )

    match = find_screen_in_reference(
        screen=screen,
        reference_path=reference_path,
    )

    assert match.found is True
    assert match.x == 20
    assert match.y == 10
    assert match.width == 50
    assert match.height == 50

def test_find_screen_in_reference_returns_not_found_when_confidence_is_too_low(
    tmp_path: Path,
):
    reference = Image.new(
        "RGB",
        (100, 80),
        "black",
    )

    for x in range(20, 40):
        for y in range(20, 40):
            reference.putpixel(
                (x, y),
                (255, 255, 255),
            )

    reference_path = (
        tmp_path
        / "reference.png"
    )

    reference.save(
        reference_path,
    )

    screen_image = Image.new(
        "RGB",
        (50, 50),
        "black",
    )

    for x in range(5, 25):
        for y in range(5, 25):
            screen_image.putpixel(
                (x, y),
                (255, 0, 0),
            )

    screen = Screen(
        screen_image,
    )

    match = find_screen_in_reference(
        screen=screen,
        reference_path=reference_path,
        confidence=0.95,
    )

    assert match.found is False
