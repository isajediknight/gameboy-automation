from pathlib import Path

import pytest
from PIL import Image

from gameboy_automation.vision.screen import Screen


def test_find_template_rejects_confidence_below_zero(
    tmp_path: Path,
) -> None:
    screen = Screen(
        Image.new(
            mode="RGB",
            size=(20, 20),
            color=(255, 255, 255),
        )
    )

    template_path = tmp_path / "template.png"

    Image.new(
        mode="RGB",
        size=(4, 4),
        color=(0, 0, 0),
    ).save(template_path)

    with pytest.raises(
        ValueError,
        match="confidence must be between 0.0 and 1.0",
    ):
        screen.find_template(
            template_path=template_path,
            confidence=-0.01,
        )


def test_find_template_rejects_confidence_above_one(
    tmp_path: Path,
) -> None:
    screen = Screen(
        Image.new(
            mode="RGB",
            size=(20, 20),
            color=(255, 255, 255),
        )
    )

    template_path = tmp_path / "template.png"

    Image.new(
        mode="RGB",
        size=(4, 4),
        color=(0, 0, 0),
    ).save(template_path)

    with pytest.raises(
        ValueError,
        match="confidence must be between 0.0 and 1.0",
    ):
        screen.find_template(
            template_path=template_path,
            confidence=1.01,
        )


def test_find_template_rejects_missing_template(
    tmp_path: Path,
) -> None:
    screen = Screen(
        Image.new(
            mode="RGB",
            size=(20, 20),
            color=(255, 255, 255),
        )
    )

    missing_template_path = tmp_path / "missing.png"

    with pytest.raises(
        FileNotFoundError,
        match="Template image not found",
    ):
        screen.find_template(
            template_path=missing_template_path,
        )


def test_find_template_rejects_template_larger_than_screen(
    tmp_path: Path,
) -> None:
    screen = Screen(
        Image.new(
            mode="RGB",
            size=(20, 20),
            color=(255, 255, 255),
        )
    )

    template_path = tmp_path / "large-template.png"

    Image.new(
        mode="RGB",
        size=(21, 20),
        color=(0, 0, 0),
    ).save(template_path)

    with pytest.raises(
        ValueError,
        match="Template dimensions cannot exceed screen dimensions",
    ):
        screen.find_template(
            template_path=template_path,
        )