
import os

from dotenv import load_dotenv

load_dotenv()


def explain_quality_failure(error_message: str) -> str:
    """Use Vertex AI Gemini to explain a data-quality failure."""
    from google import genai
    from google.genai import types

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is not configured.")

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )

    prompt = f"""
    You are a healthcare data-quality analyst.

    Explain the following validation error:
    {error_message}

    Provide:
    1. Likely cause
    2. Business impact
    3. Suggested remediation

    Do not invent patient information.
    """

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2
        ),
    )

    return response.text or "No explanation generated."


if __name__ == "__main__":
    example_error = "Negative claim amount detected in encounter E1011."

    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("Gemini integration configured in code.")
        print("Set up GCP credentials and project settings to execute.")
    else:
        print(explain_quality_failure(example_error))
