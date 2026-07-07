import json
from pathlib import Path

from app.models.mto import MTOResponse


def get_mock_mto() -> MTOResponse:
    sample_path = Path(__file__).resolve().parents[2] / "sample_mto.json"

    with open(sample_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return MTOResponse(**data)