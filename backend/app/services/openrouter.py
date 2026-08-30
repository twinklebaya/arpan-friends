"""Thin OpenRouter client used for two assistive (never-autonomous) jobs:

1. Classifying a pasted official-source update into a feed item + optional
   suggested person-status change (still requires admin approval).
2. Triaging a public tip submission for spam/duplicate likelihood before it
   reaches the human review queue (never auto-publishes anything).

If OPENROUTER_API_KEY is unset, both functions return a stub result flagged
`ai_error` so the caller can fall back to "needs manual review" instead of
failing the request.
"""

import json
from typing import Optional

import httpx

from ..config import get_settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

_SOURCE_SYSTEM_PROMPT = """You are a careful triage assistant for a disaster-response site \
tracking a tour group missing after flash floods. You NEVER decide anything on your own; you \
only propose a structured classification for a human admin to approve or reject.

Given a pasted excerpt (which may be from an official government/embassy source, an established \
news outlet, or an unverified social media post) and a list of currently-tracked named \
individuals, respond with ONLY a JSON object:
{
  "feed_type": "general" or "target",
  "summary": "one or two neutral sentences summarizing the update",
  "person_match_name": "<exact name from the provided list, or null>",
  "status_suggestion": "missing" or "deceased" or null,
  "stats_note": "<short note about rescued/total counts if mentioned, or null>",
  "confidence": <0.0-1.0>
}

Rules:
- "target" feed_type means the excerpt is specifically about the Kailash Journeys group or one \
of the named individuals. Otherwise use "general".
- Only set status_suggestion to "deceased" if the source excerpt explicitly and unambiguously \
confirms that specific person's death. If there is any ambiguity, leave it null and lower \
confidence.
- If the excerpt is from an unverified social media post (source_type "social_media"), NEVER set \
status_suggestion to "deceased" even if the post claims it -- a death determination from social \
media alone is not reliable enough. Set it to null and note the claim in "summary" instead so a \
human reviewer can seek official corroboration.
- person_match_name must be copied exactly from the provided list, or null if no clear match.
- Output raw JSON only, no markdown fences, no commentary."""

_TIP_SYSTEM_PROMPT = """You are a spam/quality triage assistant for public tip submissions on a \
missing-persons crisis site. You do not approve or reject anything yourself; you only annotate \
for a human reviewer. Given the tip text, respond with ONLY a JSON object:
{"spam_likelihood": <0.0-1.0>, "notes": "<one short sentence, e.g. 'looks like an unrelated ad' \
or 'plausible eyewitness account, no red flags'>"}
Output raw JSON only, no markdown fences, no commentary."""


async def _call_openrouter(system_prompt: str, user_content: str) -> Optional[dict]:
    settings = get_settings()
    if not settings.openrouter_api_key:
        return None

    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.1,
    }
    headers = {"Authorization": f"Bearer {settings.openrouter_api_key}"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    raw = data["choices"][0]["message"]["content"].strip()
    # Models sometimes wrap JSON in ```json fences despite instructions.
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


async def classify_source_update(
    raw_text: str, source_name: str, source_type: str, known_target_names: list[str]
) -> dict:
    user_content = (
        f"Source: {source_name}\n"
        f"source_type: {source_type}\n"
        f"Known tracked individuals: {', '.join(known_target_names) or '(none loaded)'}\n\n"
        f"Excerpt:\n{raw_text}"
    )
    try:
        result = await _call_openrouter(_SOURCE_SYSTEM_PROMPT, user_content)
    except Exception as exc:  # network/parse failure -> manual review fallback
        return {"ai_error": f"OpenRouter call failed: {exc}"}

    if result is None:
        return {"ai_error": "OPENROUTER_API_KEY not configured; manual classification required."}
    return result


async def moderate_tip(message: str) -> dict:
    try:
        result = await _call_openrouter(_TIP_SYSTEM_PROMPT, message)
    except Exception as exc:
        return {"ai_error": f"OpenRouter call failed: {exc}"}

    if result is None:
        return {"ai_error": "OPENROUTER_API_KEY not configured; manual moderation required."}
    return result
