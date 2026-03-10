from google import genai
from google.genai import types
import os
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

_client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.0-flash"  # Use a Gemini 2.0 model optimized for code generation 


def generate_sql(user_prompt: str, system_prompt: str) -> str:
    """
    Sends system + user prompt to Gemini and returns a clean SQL query.
    """
    response = _client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )
    text = response.text.strip()
    # Strip markdown code fences if present
    text = re.sub(r"```sql\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```\s*", "", text)
    return text.strip()
