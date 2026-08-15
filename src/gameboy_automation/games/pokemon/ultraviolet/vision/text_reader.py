"""Utilities for reading Pokémon Ultra Violet text from screen regions."""

from pathlib import Path

from PIL import Image

from gameboy_automation.games.pokemon.ultraviolet.vision.number_reader import (
    _matches_template,
    _pixel_category,
    _normalized_pixels,
)
from gameboy_automation.vision import Screen


LETTER_TEMPLATE_DIRECTORY = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "letters"
)


class TextRecognitionError(ValueError):
    """Raised when text cannot be recognized from a screen region."""


def read_text(
    screen: Screen,
) -> str:
    """Read uppercase Ultra Violet text from a screen region."""
    characters: list[str] = []
    x = 0

    while x < screen.width:
        matched_character: str | None = None
        matched_width: int | None = None

        for character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            template_path = (
                LETTER_TEMPLATE_DIRECTORY
                / f"{character.lower()}.png"
            )

            if not template_path.exists():
                continue

            template_image = Image.open(
                template_path
            ).convert("RGB")

            right = x + template_image.width

            if right > screen.width:
                continue

            if template_image.height > screen.height:
                continue

            for top in range(
                screen.height - template_image.height + 1
            ):
                candidate = screen.crop(
                    left=x,
                    top=top,
                    right=right,
                    bottom=top + template_image.height,
                )

                matches = _matches_template(
                    candidate.image,
                    template_image,
                )

                if matches:
                    matched_character = character
                    matched_width = template_image.width
                    break

            if matched_character is not None:
                break

        if matched_character is not None:
            characters.append(
                matched_character
            )

            assert matched_width is not None

            x += matched_width
            continue

        column_has_glyph = False

        for y in range(screen.height):
            pixel = screen.pixel(
                x,
                y,
            )

            if _pixel_category(
                (
                    pixel.red,
                    pixel.green,
                    pixel.blue,
                )
            ) != 0:
                column_has_glyph = True
                break

        if column_has_glyph:
            raise TextRecognitionError(
                f"Could not recognize character beginning at x={x}."
            )

        x += 1

    if not characters:
        raise TextRecognitionError(
            "Could not recognize Ultra Violet text."
        )

    return "".join(characters)