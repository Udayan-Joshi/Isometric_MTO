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
        import fitz

        document = fitz.open(stream=file_bytes, filetype="pdf")
        if document.page_count == 0:
            raise ValueError("Unable to read PDF.")

        page = document.load_page(0)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(3, 3))
        image = Image.open(BytesIO(pixmap.tobytes("png")))
        document.close()

    image = image.convert("RGB")

    image.thumbnail((2000, 2000))

    return image