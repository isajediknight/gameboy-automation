from PIL import Image

import bootstrap

from gameboy_automation.games.pokemon.ultraviolet.vision.number_reader import (
    DIGIT_TEMPLATE_DIRECTORY,
    read_digit,
    read_number,
    read_number_auto,
)
from gameboy_automation.vision import Screen


def test_read_digit_recognizes_zero():
    image = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "0.png"
    )

    screen = Screen(image)

    assert read_digit(screen) == 0


def test_read_digit_recognizes_one():
    image = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "1.png"
    )

    screen = Screen(image)

    assert read_digit(screen) == 1


def test_read_digit_recognizes_nine():
    image = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "9.png"
    )

    screen = Screen(image)

    assert read_digit(screen) == 9

def test_read_number_recognizes_28():
    digit_2 = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "2.png"
    ).convert("RGB")

    digit_8 = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "8.png"
    ).convert("RGB")

    image = Image.new(
        "RGB",
        (
            digit_2.width + digit_8.width,
            digit_2.height,
        ),
    )

    image.paste(
        digit_2,
        (0, 0),
    )

    image.paste(
        digit_8,
        (digit_2.width, 0),
    )

    screen = Screen(image)

    assert read_number(
        screen,
        digit_widths=[
            digit_2.width,
            digit_8.width,
        ],
    ) == 28


def test_read_number_supports_narrow_digit_one():
    digit_1 = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "1.png"
    ).convert("RGB")

    digit_0 = Image.open(
        DIGIT_TEMPLATE_DIRECTORY
        / "0.png"
    ).convert("RGB")

    image = Image.new(
        "RGB",
        (
            digit_1.width + digit_0.width,
            digit_1.height,
        ),
    )

    image.paste(
        digit_1,
        (0, 0),
    )

    image.paste(
        digit_0,
        (digit_1.width, 0),
    )

    screen = Screen(image)

    assert read_number(
        screen,
        digit_widths=[
            digit_1.width,
            digit_0.width,
        ],
    ) == 10

def test_read_number_auto_recognizes_real_level_28():
    image = Image.open(
        "tests/assets/ultraviolet/level_28.png"
    )

    screen = Screen(image)

    assert read_number_auto(screen) == 28