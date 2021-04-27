from io import BytesIO

from PIL import Image


def convert_bytes_to_rgb_image(image_bytes: bytes) -> Image:
    image = Image.open(BytesIO(image_bytes))
    return image.convert('RGB')


def convert_expected_image_to_rgb(filename: str, img_size: str) -> Image:
    image = Image.open(f'tests/input_pics/{filename}')
    if img_size != 'original':
        image = image.resize((int(img_size), int(img_size)))
    return image.convert('RGB')
