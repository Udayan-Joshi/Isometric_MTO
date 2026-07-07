from io import BytesIO
from typing import BinaryIO

from PIL import Image
from pdf2image import convert_from_bytes


def load_image(file_bytes: bytes, content_type: str) -> Image.Image:
    """
    Convert uploaded file into a PIL Image.
    Supports PNG, JPG and PDF.
    """

    if content_type == "application/pdf":
        pages = convert_from_bytes(file_bytes)

        if not pages:
            raise ValueError("Unable to read PDF.")

        image = pages[0]

    else:
        image = Image.open(BytesIO(file_bytes))

    image = image.convert("RGB")

    image.thumbnail((2000, 2000))

    return image