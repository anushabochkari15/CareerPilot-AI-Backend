"""
CareerPilot AI — Prompt Templates

Centralized imports for all prompt templates used in the AI service layer.
"""

from app.prompts.resume_prompt import RESUME_ANALYSIS_PROMPT
from app.prompts.roadmap_prompt import CAREER_ROADMAP_PROMPT
from app.prompts.interview_prompt import INTERVIEW_PROMPT
from app.prompts.project_prompt import PROJECT_PROMPT
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.prompts.chat_prompt import CHAT_PROMPT

__all__ = [
    "RESUME_ANALYSIS_PROMPT",
    "CAREER_ROADMAP_PROMPT",
    "INTERVIEW_PROMPT",
    "PROJECT_PROMPT",
    "PLANNER_PROMPT",
    "CHAT_PROMPT",
]
