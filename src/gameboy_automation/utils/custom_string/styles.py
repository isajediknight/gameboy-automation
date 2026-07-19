from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional


@dataclass(frozen=True)
class RGBColor:
    """Immutable RGB color + ANSI parameters."""

    name: str
    red: int
    green: int
    blue: int
    ansi_1: str = "0"
    ansi_2: str = "38"
    ansi_3: str = "2"

    def clamp(self) -> "RGBColor":
        def _clamp(x: int) -> int:
            return max(0, min(255, int(x)))

        return replace(self, red=_clamp(self.red), green=_clamp(self.green), blue=_clamp(self.blue))


@dataclass(frozen=True)
class TextStyle:
    """Style container. Extend later (bold, underline, bg color, etc.)."""

    color: Optional[RGBColor] = None
