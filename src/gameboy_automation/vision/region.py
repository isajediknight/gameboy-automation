from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from typing import TYPE_CHECKING
from .template_matching import TemplateMatch

if TYPE_CHECKING:
    from .screen import Screen

@dataclass(frozen=True)
class Region:
    """
    Represents a rectangular portion of a Screen.
    """

    screen: "Screen"
    x: int
    y: int
    width: int
    height: int

    @property
    def image(self):
        """
        Returns the cropped PIL image for this region.
        """
        return self.screen.image.crop(
            (
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height,
            )
        )

    def pixel(
        self,
        x: int,
        y: int,
    ):
        """
        Returns the pixel at coordinates relative to this region.
        """
        return self.screen.pixel(
            self.x + x,
            self.y + y,
        )

    def save(
        self,
        filename: str | Path,
    ) -> None:
        """
        Saves this region as an image.
        """
        self.image.save(filename)

    def find_template(
        self,
        template_path: str | Path,
        confidence: float = 0.95,
    ) -> TemplateMatch:
        """
        Searches only this region for the template.
        """
        from .screen import Screen
        cropped_screen = Screen(self.image)

        return cropped_screen.find_template(
            template_path=template_path,
            confidence=confidence,
        )