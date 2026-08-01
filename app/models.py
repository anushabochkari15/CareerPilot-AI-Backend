"""
CareerPilot AI — Pydantic Models / Schemas

Request and response models for all API endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ─── Resume Analysis ────────────────────────────────────────────────────────

class ResumeAnalysisResponse(BaseModel):
    name: str
    contact: str
    ats_score: int = Field(ge=0, le=100)
    strengths: List[str]
    weaknesses: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    keywords_found: List[str]
    keywords_missing: List[str]
    summary: str


# ─── Career Roadmap ──────────────────────────────────────────────────────────

class RoadmapRequest(BaseModel):
    year: str = Field(..., description="Current academic year")
    branch: str = Field(..., description="Engineering branch")
    skills: str = Field(..., description="Comma-separated current skills")
    goal: str = Field(..., description="Career goal / target role")
    time: str = Field(..., description="Available time for preparation")

    class Config:
        json_schema_extra = {
            "example": {
                "year": "Final Year",
                "branch": "Computer Science",
                "skills": "Python, HTML, CSS",
                "goal": "Full Stack Developer",
                "time": "4 months",
            }
        }


class Course(BaseModel):
    title: str
    platform: str
    url: str


class Certification(BaseModel):
    title: str
    provider: str


class RoadmapPhase(BaseModel):
    phase: str
    duration: str
    focus: str
    skills: List[str]
    courses: List[Course]
    certifications: List[Certification]
    projects: List[str]
    milestones: List[str]


class RoadmapResponse(BaseModel):
    goal: str
    total_duration: str
    phases: List[RoadmapPhase]
    recommended_courses: List[Course]
    recommended_certifications: List[Certification]
    recommended_projects: List[str]
    timeline: List[dict]


# ─── Interview Prep ─────────────────────────────────────────────────────────

class InterviewRequest(BaseModel):
    role: str = Field(..., description="Target job role")
    types: List[str] = Field(default=["Technical"], description="Question types: Technical, HR, Behavioral, Coding")
    difficulty: str = Field(default="Mixed", description="Beginner, Intermediate, Advanced, or Mixed")
    count: int = Field(default=8, ge=1, le=20, description="Number of questions")


class InterviewQuestion(BaseModel):
    question: str
    type: str
    difficulty: str
    hint: str
    answer: str
    topics: List[str]


class InterviewResponse(BaseModel):
    role: str
    questions: List[InterviewQuestion]
    tips: List[str]


# ─── Project Recommendation ──────────────────────────────────────────────────

class ProjectRequest(BaseModel):
    goal: str = Field(..., description="Career goal")
    skills: str = Field(..., description="Comma-separated current skills")
    interest: str = Field(default="", description="Area of interest")
    difficulty: str = Field(default="Mixed", description="Beginner, Intermediate, Advanced, or Mixed")


class Resource(BaseModel):
    title: str
    url: str


class ProjectIdea(BaseModel):
    title: str
    description: str
    difficulty: str
    tech_stack: List[str]
    architecture: str
    features: List[str]
    learning_outcomes: List[str]
    resources: List[Resource]
    estimated_time: str


class ProjectResponse(BaseModel):
    goal: str
    projects: List[ProjectIdea]


# ─── Learning Planner ────────────────────────────────────────────────────────

class PlannerRequest(BaseModel):
    duration: str = Field(..., description="30, 60, or 90 days")
    hours_per_day: int = Field(default=3, ge=1, le=12)
    goal: str = Field(..., description="Career goal")
    start_date: str = Field(..., description="ISO date string YYYY-MM-DD")


class PlannerDay(BaseModel):
    day: int
    date: str
    topic: str
    tasks: List[str]
    hours: int
    type: str


class PlannerWeek(BaseModel):
    week: int
    days: List[PlannerDay]
    goal: str
    progress: int


class PlannerResponse(BaseModel):
    duration: str
    start_date: str
    weeks: List[PlannerWeek]
    daily_hours: int
    total_hours: int


# ─── Chat ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    history: Optional[List[dict]] = Field(default=[], description="Conversation history")


class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    timestamp: int


# ─── History ──────────────────────────────────────────────────────────────────

class HistoryEntry(BaseModel):
    id: str
    feature: str
    title: str
    summary: str
    data: dict
    created_at: str


class HistoryCreateRequest(BaseModel):
    feature: str
    title: str
    summary: str
    data: dict
