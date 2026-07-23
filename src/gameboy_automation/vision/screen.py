from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


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