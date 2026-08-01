from PIL import Image


def extract_game_viewport(
    image: Image.Image,
) -> Image.Image:
    """
    Extract the 3:2 Game Boy Advance viewport from an mGBA client image.
    """
    viewport_width = image.width
    viewport_height = viewport_width * 2 // 3

    if viewport_height > image.height:
        raise ValueError(
            "Client image is too short to contain a 3:2 GBA viewport."
        )

    top = image.height - viewport_height

    return image.crop(
        (
            0,
            top,
            viewport_width,
            image.height,
        )
    )