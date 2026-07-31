"""
CareerPilot AI — AI Service Layer

Interfaces with Google Gemini API for all AI-powered features.
Handles structured output generation, error handling, and fallbacks.
"""

import json
import logging
from typing import Optional

import google.generativeai as genai

from app.config import settings
from app.prompts import (
    RESUME_ANALYSIS_PROMPT,
    CAREER_ROADMAP_PROMPT,
    INTERVIEW_PROMPT,
    PROJECT_PROMPT,
    PLANNER_PROMPT,
    CHAT_PROMPT,
)

logger = logging.getLogger(__name__)

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

# Model configuration
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


def _get_model(model_name: str = "gemini-1.5-flash"):
    """Get a Gemini model instance."""
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
    )


def _parse_json_response(text: str) -> dict:
    """Extract and parse JSON from a Gemini response, handling markdown code blocks."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```json or ```) and last line (```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        raise ValueError(f"AI returned invalid JSON: {e}")


async def analyze_resume(resume_text: str) -> dict:
    """Analyze resume text and return structured analysis."""
    prompt = RESUME_ANALYSIS_PROMPT.format(resume_text=resume_text)
    return await _generate_structured(prompt)


async def generate_roadmap(
    year: str, branch: str, skills: str, goal: str, time: str
) -> dict:
    """Generate a career roadmap."""
    prompt = CAREER_ROADMAP_PROMPT.format(
        year=year, branch=branch, skills=skills, goal=goal, time=time
    )
    return await _generate_structured(prompt)


async def generate_interview_questions(
    role: str, types: list, difficulty: str, count: int
) -> dict:
    """Generate interview preparation questions."""
    prompt = INTERVIEW_PROMPT.format(
        role=role, types=", ".join(types), difficulty=difficulty, count=count
    )
    return await _generate_structured(prompt)


async def recommend_projects(
    goal: str, skills: str, interest: str, difficulty: str
) -> dict:
    """Recommend portfolio projects."""
    prompt = PROJECT_PROMPT.format(
        goal=goal, skills=skills, interest=interest, difficulty=difficulty
    )
    return await _generate_structured(prompt)


async def generate_planner(
    duration: str, hours_per_day: int, goal: str, start_date: str
) -> dict:
    """Generate a learning plan."""
    prompt = PLANNER_PROMPT.format(
        duration=duration,
        hours_per_day=hours_per_day,
        goal=goal,
        start_date=start_date,
    )
    return await _generate_structured(prompt)


async def generate_chat_response(message: str, history: list) -> str:
    """Generate a chat response (returns plain text, not JSON)."""
    history_text = "\n".join(
        [f"{'User' if m.get('role') == 'user' else 'Assistant'}: {m.get('content', '')}" for m in history[-10:]]
    )
    prompt = CHAT_PROMPT.format(history=history_text, message=message)

    try:
        if not settings.GEMINI_API_KEY:
            return "AI service is not configured. Please set GEMINI_API_KEY in your .env file."

        model = _get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Chat generation failed: {e}")
        return f"I apologize, but I encountered an error: {str(e)}. Please try again."


async def _generate_structured(prompt: str) -> dict:
    """Generate structured JSON output from Gemini."""
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Set it in your .env file."
        )

    try:
        model = _get_model()
        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("AI returned an empty response")

        return _parse_json_response(response.text)
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        raise
