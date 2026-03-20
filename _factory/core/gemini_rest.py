"""
Lightweight Gemini REST client — no SDK required.
Returns content + token usage metadata for cost tracking.
"""
import json
import os
import requests


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def call_gemini(prompt, model="gemini-2.0-flash", is_json=False):
    """
    Call Gemini via REST API.

    Returns:
        dict: {"content": parsed result, "input_tokens": int, "output_tokens": int}
        None on failure.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set")

    url = GEMINI_API_URL.format(model=model) + f"?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
        },
    }

    if is_json:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})

        parsed = text
        if is_json:
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(text)

        return {
            "content": parsed,
            "input_tokens": usage.get("promptTokenCount", 0),
            "output_tokens": usage.get("candidatesTokenCount", 0),
        }

    except requests.exceptions.HTTPError as e:
        print(f"[GEMINI ERROR] HTTP {e.response.status_code}: {e.response.text[:200]}")
        return None
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"[GEMINI ERROR] Parse error: {e}")
        return None
    except Exception as e:
        print(f"[GEMINI ERROR] {e}")
        return None
