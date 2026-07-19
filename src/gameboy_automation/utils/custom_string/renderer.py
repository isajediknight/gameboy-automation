from __future__ import annotations

from .styles import RGBColor, TextStyle


class AnsiRenderer:
    """Renders text with optional ANSI TrueColor.

    If you prefer your own TextColor class, swap the implementation of
    `render_colored()` to construct and return that object as a string.
    """

    @staticmethod
    def render_plain(text: str) -> str:
        return text

    @staticmethod
    def render_colored(text: str, color: RGBColor) -> str:
        c = color.clamp()
        # Standard ANSI TrueColor:
        # ESC[0;38;2;R;G;Bm ... ESC[0m
        return f"\033[{c.ansi_1};{c.ansi_2};{c.ansi_3};{c.red};{c.green};{c.blue}m{text}\033[0m"

    def render(self, text: str, style: TextStyle) -> str:
        if style.color is None:
            return self.render_plain(text)
        return self.render_colored(text, style.color)
