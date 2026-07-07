import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.mto import MTOResponse
from app.services.mock_service import get_mock_mto

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

print("API Key Loaded:", bool(API_KEY))
print("Model:", MODEL_NAME)

class GeminiService:
    def __init__(self):
        self.client = None

        if API_KEY:
            self.client = genai.Client(api_key=API_KEY)

        prompt_path = (
            Path(__file__).resolve().parents[1]
            / "prompts"
            / "extraction_prompt.txt"
        )

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt = f.read()

    def extract(self, image):
        """
        Returns validated MTOResponse.

        Falls back to mock mode if:
        - API key missing
        - Gemini fails
        """

        if not self.client:
            return get_mock_mto()

        try:

            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    self.prompt,
                    image,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )

            data = json.loads(response.text)

            return MTOResponse(**data)

        except Exception as e:
            print("Gemini Error:", e)
            return get_mock_mto()