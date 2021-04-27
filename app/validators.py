from io import BytesIO

from PIL import Image, UnidentifiedImageError


def check_if_image_is_square(file: bytes) -> bool:
    image = Image.open(BytesIO(file))
    width, height = image.size
    return width == height


def check_if_file_is_image(file: bytes) -> bool:
    try:
        Image.open(BytesIO(file))
        return True
    except UnidentifiedImageError:
        return False
