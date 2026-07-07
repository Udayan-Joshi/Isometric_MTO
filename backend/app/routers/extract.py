from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.models.mto import MTOResponse
from app.services.mock_service import get_mock_mto
from app.services.csv_service import generate_csv

router = APIRouter(prefix="/api", tags=["MTO"])

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
}

MAX_SIZE = 20 * 1024 * 1024  # 20 MB

# Stores the most recent extraction result
latest_result: MTOResponse | None = None


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post("/extract", response_model=MTOResponse)
async def extract(file: UploadFile = File(...)):
    global latest_result

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG and PDF files are allowed."
        )

    # Read uploaded file
    contents = await file.read()

    # Validate file size
    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 20 MB."
        )

    # --------------------------------------------------
    # Current pipeline
    # --------------------------------------------------
    # Mock pipeline (Gemini integration can replace this later)
    latest_result = get_mock_mto()

    return latest_result


@router.get("/export/csv")
def export_csv():
    if latest_result is None:
        raise HTTPException(
            status_code=404,
            detail="No extraction available. Upload a drawing first."
        )

    csv_data = generate_csv(latest_result)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="mto.csv"'
        },
    )