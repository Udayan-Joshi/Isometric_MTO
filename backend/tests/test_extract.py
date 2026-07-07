from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_extract_png():
    image = BytesIO(b"fake image data")

    response = client.post(
        "/api/extract",
        files={
            "file": (
                "test.png",
                image,
                "image/png",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "drawing_meta" in data
    assert "items" in data
    assert "summary" in data