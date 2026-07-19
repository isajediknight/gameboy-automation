from __future__ import annotations

from typing import Any, Optional

from .classifier import ClassificationResult, ValueClassifier
from .renderer import AnsiRenderer
from .styles import RGBColor, TextStyle


class CustomString:
    """CustomString

    - `+` / `r+` return CustomString (chainable)
    - `str(custom)` renders with ANSI if color exists
    - padding computed at render time (no fix_spacing required)
    - type detection delegated to ValueClassifier
    """

    def __init__(
        self,
        value: Any,
        *,
        style: Optional[TextStyle] = None,
        prepend_width: int = 0,
        postpend_spaces: int = 0,
        renderer: Optional[AnsiRenderer] = None,
    ):
        self.value: str = "" if value is None else str(value)

        # spacing settings
        self.prepend_width: int = int(prepend_width)      # target total width by LEFT-padding
        self.postpend_spaces: int = int(postpend_spaces)  # add N spaces to the right

        # style + renderer
        self.style: TextStyle = style or TextStyle()
        self._renderer: AnsiRenderer = renderer or AnsiRenderer()

        # classification output (populated by identify_type())
        self._classification: ClassificationResult = ClassificationResult()

    # -------------------------
    # Backwards-compat methods
    # -------------------------
    def define_color(
        self,
        name: str,
        red: int,
        green: int,
        blue: int,
        ansi_1: str = "0",
        ansi_2: str = "38",
        ansi_3: str = "2",
    ) -> None:
        self.style = TextStyle(color=RGBColor(name, red, green, blue, ansi_1, ansi_2, ansi_3))

    def define_color_replace_text(
        self,
        name: str,
        red: int,
        green: int,
        blue: int,
        text: str,
        ansi_1: str = "0",
        ansi_2: str = "38",
        ansi_3: str = "2",
    ) -> None:
        self.define_color(name, red, green, blue, ansi_1, ansi_2, ansi_3)
        self.value = str(text)

    def set_pre_spaces(self, prepend_spaces: int) -> None:
        self.prepend_width = int(prepend_spaces)

    def set_post_spaces(self, postpend_spaces: int) -> None:
        self.postpend_spaces = int(postpend_spaces)

    def fix_spacing(self) -> None:
        # no-op, spacing computed on render
        return

    def new_text(self, text: str) -> "CustomString":
        return self.nt(text)

    def replace_text(self, text: Any) -> "CustomString":
        """
        Replace the current text IN PLACE (mutating), preserving style/padding.
        Returns self for fluent chaining.
        """
        self.value = "" if text is None else str(text)
        self._classification = ClassificationResult()
        return self

    def rt(self, text: Any) -> "CustomString":
        """Short alias for replace_text()."""
        return self.replace_text(text)


    def nt(self, text: str) -> "CustomString":
        return self._clone_with(value=str(text))

    def uncolored(self) -> str:
        # plain (no ANSI) with padding
        return self._pad(self.value)

    def c(self) -> str:
        # colored rendering (or plain if no color)
        return str(self)

    def reset_value(self, value: Any) -> None:
        # Reset only value; keep style/padding unless you want full reset
        self.value = "" if value is None else str(value)
        self._classification = ClassificationResult()

    def set_color(self, color: RGBColor) -> "CustomString":
        self.style = TextStyle(color=color)
        return self

    # -------------------------
    # Core behavior
    # -------------------------
    def _clone_with(
        self,
        *,
        value: Optional[str] = None,
        style: Optional[TextStyle] = None,
        prepend_width: Optional[int] = None,
        postpend_spaces: Optional[int] = None,
    ) -> "CustomString":
        return CustomString(
            self.value if value is None else value,
            style=self.style if style is None else style,
            prepend_width=self.prepend_width if prepend_width is None else int(prepend_width),
            postpend_spaces=self.postpend_spaces if postpend_spaces is None else int(postpend_spaces),
            renderer=self._renderer,
        )

    def _pad(self, s: str) -> str:
        left = ""
        if self.prepend_width > 0:
            missing = self.prepend_width - len(s)
            if missing > 0:
                left = " " * missing
        right = " " * self.postpend_spaces if self.postpend_spaces > 0 else ""
        return f"{left}{s}{right}"

    def render(self) -> str:
        # pad raw, then apply ANSI to include padding in color (matches prior behavior)
        padded_raw = self._pad(self.value)
        return self._renderer.render(padded_raw, self.style)

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"value={self.value!r}, "
            f"prepend_width={self.prepend_width}, "
            f"postpend_spaces={self.postpend_spaces}, "
            f"style={self.style!r})"
        )

    # -------------------------
    # Operators (return CustomString)
    # -------------------------
    def __add__(self, other: Any) -> "CustomString":
        other_str = other.render() if isinstance(other, CustomString) else str(other)
        return self._clone_with(value=self.value + other_str)

    def __radd__(self, other: Any) -> "CustomString":
        other_str = other.render() if isinstance(other, CustomString) else str(other)
        return self._clone_with(value=other_str + self.value)

    # -------------------------
    # Classification (delegated)
    # -------------------------
    def identify_type(self) -> None:
        self._classification = ValueClassifier.classify(self.value)

    # Backwards-compatible flag properties
    @property
    def VALID_PHONE_NUMBER(self) -> bool:
        return self._classification.valid_phone_number

    @property
    def IS_FILE(self) -> bool:
        return self._classification.is_file

    @property
    def IS_DIRECTORY(self) -> bool:
        return self._classification.is_directory

    @property
    def IS_DATE(self) -> bool:
        return self._classification.is_date

    @property
    def date(self):
        return self._classification.date

    @property
    def location_city(self) -> str:
        return self._classification.location_city

    @property
    def location_state_territory(self) -> str:
        return self._classification.location_state_territory

    @property
    def location_region(self) -> str:
        return self._classification.location_region

    @property
    def location_country(self) -> str:
        return self._classification.location_country

    # -------------------------
    # Debug helper
    # -------------------------
    def debug(self) -> None:
        base = self.c() + "\t"
        if self.style.color is None:
            print(base + "(no color defined)")
            return

        r = self.style.color.red
        g = self.style.color.green
        b = self.style.color.blue

        red_color = CustomString("Red"); red_color.define_color("red", r, 0, 0)
        green_color = CustomString("Green"); green_color.define_color("green", 0, g, 0)
        blue_color = CustomString("Blue"); blue_color.define_color("blue", 0, 0, b)

        red_number = CustomString(str(r), prepend_width=3)
        green_number = CustomString(str(g), prepend_width=3)
        blue_number = CustomString(str(b), prepend_width=3)

        print(
            base
            + str(red_color) + " " + str(red_number) + "\t"
            + str(green_color) + " " + str(green_number) + "\t"
            + str(blue_color) + " " + str(blue_number)
        )
