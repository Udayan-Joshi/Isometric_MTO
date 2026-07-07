from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response
from google.genai import types

from app.models.mto import MTOResponse
from app.services.csv_service import generate_csv
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/api", tags=["MTO"])

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
}

MAX_SIZE = 20 * 1024 * 1024  # 20 MB

latest_result: MTOResponse | None = None

gemini = GeminiService()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/extract", response_model=MTOResponse)
async def extract(file: UploadFile = File(...)):
    global latest_result

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG and PDF files are allowed.",
        )

    contents = await file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 20 MB.",
        )

    image = types.Part.from_bytes(
        data=contents,
        mime_type=file.content_type,
    )

    latest_result = gemini.extract(image)

    return latest_result


@router.get("/export/csv")
def export_csv():
    if latest_result is None:
        raise HTTPException(
            status_code=404,
            detail="No extraction available. Upload a drawing first.",
        )

    csv_data = generate_csv(latest_result)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="mto.csv"'
        },
    )