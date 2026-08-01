import bootstrap

from PIL import Image

from gameboy_automation.emulators.mgba.screenshots import (
    extract_game_viewport,
)


def test_extract_game_viewport_returns_bottom_3_to_2_region():
    image = Image.new(
        mode="RGB",
        size=(480, 340),
    )

    viewport = extract_game_viewport(image)

    assert viewport.size == (480, 320)