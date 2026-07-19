"""
Color palettes for CustomString.

Each palette exposes immutable RGBColor definitions
(e.g. TABLEAU_10, TABLEAU_20, MINECRAFT).
"""

from .tableau import TABLEAU_10, TABLEAU_20
from .minecraft import MINECRAFT, MINECRAFT_2

__all__ = [
    "TABLEAU_10",
    "TABLEAU_20",
    "MINECRAFT",
    "MINECRAFT_2",
]
