import bootstrap

from PIL import Image

from gameboy_automation.games.pokemon.ultraviolet.vision.text_reader import (
    LETTER_TEMPLATE_DIRECTORY,
    TextRecognitionError,
    read_text,
)
from gameboy_automation.vision import Screen


def test_text_recognition_error_is_value_error():
    assert issubclass(
        TextRecognitionError,
        ValueError,
    )


def test_read_text_recognizes_porygon():
    characters = [
        "p",
        "o",
        "r",
        "y",
        "g",
        "o",
        "n",
    ]

    images = [
        Image.open(
            LETTER_TEMPLATE_DIRECTORY
            / f"{character}.png"
        ).convert("RGB")
        for character in characters
    ]

    width = sum(
        image.width
        for image in images
    )

    height = images[0].height

    image = Image.new(
        "RGB",
        (
            width,
            height,
        ),
    )

    x = 0

    for character_image in images:
        image.paste(
            character_image,
            (x, 0),
        )

        x += character_image.width

    screen = Screen(image)

    assert read_text(screen) == "PORYGON"