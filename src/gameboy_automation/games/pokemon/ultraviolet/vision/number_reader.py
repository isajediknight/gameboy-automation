from pathlib import Path

from PIL import Image

from gameboy_automation.vision import Screen


DIGIT_TEMPLATE_DIRECTORY = (
    Path(__file__).resolve().parents[4]
    / "pokemon"
    / "assets"
    / "templates"
    / "ultraviolet"
    / "digits"
)


def _pixel_category(
    pixel: tuple[int, int, int],
) -> int:
    """
    Normalize a game-font pixel across supported screen palettes.

    Returns:
        1 for dark glyph pixels.
        2 for light glyph pixels.
        0 for background pixels.
    """
    dark_glyph_colors = {
        (99, 99, 99),
        (66, 66, 66),
        (82, 82, 82),
    }

    light_glyph_colors = {
        (255, 255, 255),
        (222, 222, 198),
        (222, 222, 222),
    }

    if pixel in dark_glyph_colors:
        return 1

    if pixel in light_glyph_colors:
        return 2

    return 0


def _normalized_pixels(
    image: Image.Image,
) -> list[int]:
    """Return a background-independent glyph mask."""
    rgb_image = image.convert("RGB")

    return [
        1 if _pixel_category(pixel) != 0 else 0
        for pixel in rgb_image.get_flattened_data()
    ]

def _matches_template(
    candidate: Image.Image,
    template: Image.Image,
) -> bool:
    """Return True when glyph shapes match with small vertical offsets."""
    candidate_pixels = _normalized_pixels(candidate)
    template_pixels = _normalized_pixels(template)

    width, height = candidate.size

    if candidate.size != template.size:
        return False

    candidate_rows = [
        candidate_pixels[
            row * width:(row + 1) * width
        ]
        for row in range(height)
    ]

    template_rows = [
        template_pixels[
            row * width:(row + 1) * width
        ]
        for row in range(height)
    ]

    if candidate_rows == template_rows:
        return True

    shifted_down = (
        [[0] * width]
        + template_rows[:-1]
    )

    return candidate_rows == shifted_down

def read_digit(screen: Screen) -> int:
    """Read one tightly cropped Ultra Violet numeric glyph."""
    for digit in range(10):
        template_path = (
            DIGIT_TEMPLATE_DIRECTORY
            / f"{digit}.png"
        )

        template_image = Image.open(template_path)

        if screen.size != template_image.size:
            continue

        if _matches_template(
            screen.image,
            template_image,
        ):
            return digit

    raise ValueError(
        "Could not recognize Ultra Violet digit."
    )

def read_number(
    screen: Screen,
    digit_widths: list[int],
) -> int:
    """
    Read a sequence of Ultra Violet numeric glyphs.

    Args:
        screen:
            Screen containing only the numeric glyphs.

        digit_widths:
            Width of each digit glyph from left to right.

    Returns:
        The recognized integer.
    """
    digits: list[str] = []

    left = 0

    for width in digit_widths:
        digit_screen = screen.crop(
            left=left,
            top=0,
            right=left + width,
            bottom=screen.height,
        )

        digit = read_digit(
            digit_screen,
        )

        digits.append(
            str(digit)
        )

        left += width

    return int(
        "".join(digits)
    )

def read_number_auto(
    screen: Screen,
) -> int:
    """
    Read an Ultra Violet number without pre-supplied digit widths.

    The reader scans left-to-right, matching each digit template
    and allowing blank background columns between digits.
    """
    digits: list[str] = []
    x = 0

    while x < screen.width:
        matched_digit: int | None = None
        matched_width: int | None = None

        for digit in range(10):
            template_path = (
                DIGIT_TEMPLATE_DIRECTORY
                / f"{digit}.png"
            )

            template_image = Image.open(
                template_path
            ).convert("RGB")

            if template_image.height != screen.height:
                continue

            right = x + template_image.width

            if right > screen.width:
                continue

            candidate = screen.crop(
                left=x,
                top=0,
                right=right,
                bottom=screen.height,
            )

            if _matches_template(
                candidate.image,
                template_image,
            ):
                matched_digit = digit
                matched_width = template_image.width
                break

        if matched_digit is not None:
            digits.append(
                str(matched_digit)
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
            raise ValueError(
                f"Could not recognize digit beginning at x={x}."
            )

        x += 1

    if not digits:
        raise ValueError(
            "Could not recognize an Ultra Violet number."
        )

    return int(
        "".join(digits)
    )