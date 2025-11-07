import vertexai
from vertexai.preview.generative_models import GenerativeModel
import json, os

vertexai.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION"))

def extract_structured_estimate(raw_text: str):
    """
    Sends extracted drawing text to Gemini to classify as beam/column with attributes.
    """
    model = GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a civil structural estimator.

    From this drawing text, extract structural elements like:
    - type (Beam/Column/Slab)
    - dimensions (width, height)
    - material
    - length if available

    Return in clean JSON list format, no explanation.

    Drawing Content:
    {raw_text}
    """

    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except Exception:
        return []
