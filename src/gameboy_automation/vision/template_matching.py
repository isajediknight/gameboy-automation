from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import cv2
import numpy as np

if TYPE_CHECKING:
    from .screen import Screen


@dataclass(frozen=True)
class TemplateMatch:
    """Result of searching for a template within a screen."""

    found: bool
    confidence: float
    x: int
    y: int
    width: int
    height: int


def find_template(
    screen: Screen,
    template_path: str | Path,
    confidence: float = 0.95,
) -> TemplateMatch:
    """
    Find an image template within a captured screen.

    Args:
        screen:
            Screen to search.
        template_path:
            Path to the template image.
        confidence:
            Minimum confidence required for a successful match.

    Returns:
        The strongest template match found on the screen.

    Raises:
        ValueError:
            If confidence is outside the range 0.0 through 1.0, or if
            the template is larger than the screen.
        FileNotFoundError:
            If the template image does not exist.
        RuntimeError:
            If OpenCV cannot load the template image.
    """
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(
            "confidence must be between 0.0 and 1.0."
        )

    resolved_template_path = Path(template_path)

    if not resolved_template_path.is_file():
        raise FileNotFoundError(
            f"Template image not found: {resolved_template_path}"
        )

    template_image = cv2.imread(
        str(resolved_template_path),
        cv2.IMREAD_COLOR,
    )

    if template_image is None:
        raise RuntimeError(
            f"OpenCV could not load template image: "
            f"{resolved_template_path}"
        )

    screen_image = np.asarray(
        screen.image.convert("RGB")
    )

    screen_image = cv2.cvtColor(
        screen_image,
        cv2.COLOR_RGB2BGR,
    )

    template_height, template_width = template_image.shape[:2]
    screen_height, screen_width = screen_image.shape[:2]

    if (
        template_width > screen_width
        or template_height > screen_height
    ):
        raise ValueError(
            "Template dimensions cannot exceed screen dimensions."
        )

    match_results = cv2.matchTemplate(
        screen_image,
        template_image,
        cv2.TM_CCOEFF_NORMED,
    )

    _, maximum_confidence, _, maximum_location = cv2.minMaxLoc(
        match_results
    )

    match_x, match_y = maximum_location

    return TemplateMatch(
        found=maximum_confidence >= confidence,
        confidence=float(maximum_confidence),
        x=match_x,
        y=match_y,
        width=template_width,
        height=template_height,
    )