from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from PIL import Image
from typing import NamedTuple
from .template_matching import find_template


class Pixel(NamedTuple):
    """RGB value of a single pixel."""

    red: int
    green: int
    blue: int

    def is_close(
        self,
        other: "Pixel",
        tolerance: int = 0,
    ) -> bool:
        """
        Return True if two pixels are within the specified RGB tolerance.
        """
        return (
            abs(self.red - other.red) <= tolerance
            and abs(self.green - other.green) <= tolerance
            and abs(self.blue - other.blue) <= tolerance
        )


@dataclass(frozen=True)
class Screen:
    """A captured emulator screen."""

    image: Image.Image

    @property
    def width(self) -> int:
        """Return the screen width in pixels."""
        return self.image.width

    @property
    def height(self) -> int:
        """Return the screen height in pixels."""
        return self.image.height

    @property
    def size(self) -> tuple[int, int]:
        """Return the screen dimensions as width and height."""
        return self.image.size

    def pixel(
        self,
        x: int,
        y: int,
    ) -> Pixel:
        """
        Return the RGB value of a single pixel.
        """
        if not (0 <= x < self.width):
            raise ValueError(
                f"x must be between 0 and {self.width - 1}."
            )

        if not (0 <= y < self.height):
            raise ValueError(
                f"y must be between 0 and {self.height - 1}."
            )

        red, green, blue = self.image.getpixel((x, y))

        return Pixel(
            red=red,
            green=green,
            blue=blue,
        )

    def pixel(
        self,
        x: int,
        y: int,
    ) -> Pixel:
        """
        Return the RGB value of a single pixel.
        """
        if not (0 <= x < self.width):
            raise ValueError(
                f"x must be between 0 and {self.width - 1}."
            )

        if not (0 <= y < self.height):
            raise ValueError(
                f"y must be between 0 and {self.height - 1}."
            )

        red, green, blue = self.image.getpixel((x, y))

        return Pixel(
            red=red,
            green=green,
            blue=blue,
        )

    def pixel_matches(
        self,
        x: int,
        y: int,
        expected: Pixel,
        tolerance: int = 0,
    ) -> bool:
        """
        Return True if the pixel at (x, y) matches the expected color.
        """
        return self.pixel(
            x,
            y,
        ).is_close(
            expected,
            tolerance=tolerance,
        )


    def find_template(self) -> None:
        """
        Find a template within this screen.

        Placeholder implementation.
        """
        return find_template(self)

    def save(self, path: str | Path) -> None:
        """Save the captured screen to disk."""
        output_path = Path(path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.image.save(output_path)

    def crop(
        self,
        left: int,
        top: int,
        right: int,
        bottom: int,
    ) -> Screen:
        """Return a cropped portion of the screen."""
        if left < 0 or top < 0:
            raise ValueError(
                "Crop coordinates cannot be negative."
            )

        if right > self.width or bottom > self.height:
            raise ValueError(
                "Crop coordinates cannot exceed screen dimensions."
            )

        if right <= left or bottom <= top:
            raise ValueError(
                "Crop must have positive width and height."
            )

        cropped_image = self.image.crop(
            (
                left,
                top,
                right,
                bottom,
            )
        )

        return Screen(cropped_image)
