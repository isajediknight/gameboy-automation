from enum import Enum


class Button(str, Enum):
    """Buttons supported by a Game Boy Advance emulator."""

    A = "a"
    B = "b"

    L = "l"
    R = "r"

    START = "start"
    SELECT = "select"

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"