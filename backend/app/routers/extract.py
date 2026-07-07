from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.mock_service import get_mock_mto
from app.services.pdf_utils import load_image
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/api", tags=["MTO"])
gemini = GeminiService()

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf"
}

MAX_SIZE = 20 * 1024 * 1024


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/extract")
async def extract(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG and PDF files are allowed."
        )

    contents = await file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 20 MB."
        )

        image = load_image(contents, file.content_type)
        result = gemini.extract(image)
        return result

    return get_mock_mto()