"""CustomString package.

Public API:
    from custom_string import CustomString, RGBColor, TextStyle, ValueClassifier, ClassificationResult
"""

from .string import CustomString
from .styles import RGBColor, TextStyle
from .classifier import ValueClassifier, ClassificationResult

__all__ = [
    "CustomString",
    "RGBColor",
    "TextStyle",
    "ValueClassifier",
    "ClassificationResult",
]
