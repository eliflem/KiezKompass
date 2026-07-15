import json
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
import streamlit as st


NEIGHBORHOODS_PATH = Path(__file__).resolve().parents[1] / "data" / "neighborhoods.json"
NEIGHBORHOODS_JSON = json.dumps(
    json.loads(NEIGHBORHOODS_PATH.read_text()),
    ensure_ascii=False,
    separators=(",", ":"),
)


def _format_history(conversation_history: list[dict[str, Any]]) -> str:
    lines: list[str] = ["Conversation so far:"]
    for message in conversation_history:
        content = message["content"]
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
        lines.append(f'{message["role"].capitalize()}: {content}')
    return "\n".join(lines)


def _build_system_prompt(current_round: int) -> str:
    return (
        "You are Kiez Compass, a Berlin neighborhood recommender.\n"
        "Use only the neighborhood dataset below.\n"
        f"Clarifying round: {current_round} of 3.\n"
        "If the conversation is missing one critical detail and the round is below 3, ask exactly one clarifying question.\n"
        "If the round is 3, or if you already have enough information, make a recommendation instead of asking more questions.\n"
        "Return JSON only. No markdown, no explanation, no extra text.\n"
        'If you need clarification, return {"action":"clarify","question":"..."}.\n'
        'If you recommend neighborhoods, return {"action":"recommend","recommendations":[{"zip_code":"...","district":"...","reason":"..."}]}.\n'
        f"Neighborhood dataset: {NEIGHBORHOODS_JSON}"
    )


def get_kiez_compass_response(
    conversation_history: list[dict[str, Any]],
    current_round: int,
) -> dict[str, Any]:
    prompt = _format_history(conversation_history)
    system_prompt = _build_system_prompt(current_round)

    with genai.Client(api_key=st.secrets["GEMINI_API_KEY"]) as client:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
            ),
        )

    parsed_response = json.loads(response.text or "{}")
    action = parsed_response.get("action")

    if action == "clarify":
        question = str(parsed_response.get("question", "")).strip()
        if not question:
            raise ValueError("Gemini returned a clarify response without a question.")
        return {"action": "clarify", "question": question}

    if action == "recommend":
        recommendations = parsed_response.get("recommendations", [])
        if not isinstance(recommendations, list) or not recommendations:
            raise ValueError("Gemini returned a recommendation response without recommendations.")

        normalized_recommendations: list[dict[str, str]] = []
        for recommendation in recommendations:
            if not isinstance(recommendation, dict):
                raise ValueError("Gemini returned an invalid recommendation entry.")

            zip_code = str(recommendation.get("zip_code", "")).strip()
            district = str(recommendation.get("district", "")).strip()
            reason = str(recommendation.get("reason", "")).strip()
            if not zip_code or not district or not reason:
                raise ValueError("Gemini returned an incomplete recommendation entry.")

            normalized_recommendations.append(
                {
                    "zip_code": zip_code,
                    "district": district,
                    "reason": reason,
                }
            )

        return {"action": "recommend", "recommendations": normalized_recommendations}

    raise ValueError("Gemini returned an unexpected JSON payload.")
