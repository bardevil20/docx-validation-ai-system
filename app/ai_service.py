import json
import os
import time
from typing import List

from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import Content, GenerateContentConfig
from google.genai.errors import APIError, ServerError
from pydantic import BaseModel

load_dotenv()


class Violation(BaseModel):
    rule_text: str
    quote: str
    explanation: str


class AnalysisResult(BaseModel):
    violations: List[Violation]


def _call_gemini(client: Client, prompt: str, max_retries: int = 5) -> str:
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.0,
                    response_mime_type="application/json",
                    response_schema=AnalysisResult,
                ),
            )
            result_dict = json.loads(response.text)
            return result_dict.get("violations", [])
        except ServerError as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Gemini API unavailable after {max_retries} retries: {e}")
            wait = 2 ** attempt
            print(f"Gemini API unavailable (attempt {attempt + 1}/{max_retries}). Retrying in {wait}s...")
            time.sleep(wait)


def analyze_rules(document_text: str, rules_text: str) -> list[dict]:
    client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = f"""
    DOCUMENT TEXT:
    ---
    {document_text}
    ---
    
    RULES TO CHECK:
    ---
    {rules_text}
    ---
    
    INSTRUCTIONS:
    1. Read the DOCUMENT TEXT thoroughly.
    2. For EACH rule in the RULES TO CHECK, scan the document for any statement that violates it.
    3. You must be strictly factual. Do not guess.
    4. If you find a violation, you MUST extract the exact quote from the document.
    5. If no rules are violated, return an empty list.
    6. Return the results in a JSON format with the following fields:
    - rule_text: the text of the rule that was violated
    - quote: the exact quote from the document that violates the rule
    - explanation: a short explanation of why the rule was violated
    """

    text = _call_gemini(client, prompt)

    return text
