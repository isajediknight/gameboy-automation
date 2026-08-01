import ctypes
from unittest.mock import patch

import bootstrap

from gameboy_automation.utils.windows import (
    RECT,
    get_client_bounds,
)


def test_get_client_bounds_returns_screen_coordinates():
    def fake_get_client_rect(
        window_handle,
        rectangle_pointer,
    ):
        rectangle = ctypes.cast(
            rectangle_pointer,
            ctypes.POINTER(RECT),
        ).contents

        rectangle.left = 0
        rectangle.top = 0
        rectangle.right = 480
        rectangle.bottom = 320

        return True

    def fake_client_to_screen(
        window_handle,
        point_pointer,
    ):
        point = point_pointer._obj

        point.x += 8
        point.y += 52

        return True

    with (
        patch(
            "gameboy_automation.utils.windows.user32.GetClientRect",
            side_effect=fake_get_client_rect,
        ),
        patch(
            "gameboy_automation.utils.windows.user32.ClientToScreen",
            side_effect=fake_client_to_screen,
        ),
    ):
        bounds = get_client_bounds(
            window_handle=123,
        )

    assert bounds == (
        8,
        52,
        488,
        372,
    )