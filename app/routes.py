"""
CareerPilot AI — API Routes

All REST API endpoints for the CareerPilot AI backend.
Organized by feature module with proper error handling.
"""

import json
import logging
from typing import Optional
from pydantic import BaseModel
from app.services.email_service import EmailService

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class EmailRequest(BaseModel):
    email: str
    username: str

from app.models import (
    ResumeAnalysisResponse,
    RoadmapRequest, RoadmapResponse,
    InterviewRequest, InterviewResponse,
    ProjectRequest, ProjectResponse,
    PlannerRequest, PlannerResponse,
    ChatRequest,
)
from app.database import get_db
from app.services import (
    analyze_resume,
    generate_roadmap,
    generate_interview_questions,
    recommend_projects,
    generate_planner,
    generate_chat_response,
    extract_text_from_pdf,
    save_history,
    get_history,
    delete_history,
)

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_MIME_TYPES = ["application/pdf"]


# ─── Resume Analysis ────────────────────────────────────────────────────────

@router.post("/resume", response_model=ResumeAnalysisResponse)
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a PDF resume and get AI-powered analysis including:
    ATS score, strengths, weaknesses, missing skills, and suggestions.
    """
    # Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Read and validate file size
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # Extract text
    resume_text = extract_text_from_pdf(file_bytes)
    if not resume_text or len(resume_text) < 50:
        raise HTTPException(
            status_code=422,
            detail="Could not extract sufficient text from PDF. The file may be scanned or image-based.",
        )

    # Analyze with AI
    try:
        result = await analyze_resume(resume_text)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


# ─── Career Roadmap ──────────────────────────────────────────────────────────

@router.post("/career-roadmap", response_model=RoadmapResponse)
async def roadmap_endpoint(request: RoadmapRequest, db: AsyncSession = Depends(get_db)):
    """Generate a personalized career roadmap based on student profile."""
    try:
        result = await generate_roadmap(
            request.year, request.branch, request.skills, request.goal, request.time
        )
        await save_history(
            db, "roadmap",
            f"Roadmap — {request.goal}",
            f"{len(result.get('phases', []))} phases over {request.time}",
            result,
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Roadmap generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate roadmap")


# ─── Interview Prep ───────────────────────────────────────────────────────────

@router.post("/interview", response_model=InterviewResponse)
async def interview_endpoint(request: InterviewRequest, db: AsyncSession = Depends(get_db)):
    """Generate interview preparation questions with hints and answers."""
    try:
        result = await generate_interview_questions(
            request.role, request.types, request.difficulty, request.count
        )
        await save_history(
            db, "interview",
            f"Interview Prep — {request.role}",
            f"{len(result.get('questions', []))} questions generated",
            result,
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Interview generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate questions")


# ─── Project Recommendation ──────────────────────────────────────────────────

@router.post("/projects", response_model=ProjectResponse)
async def projects_endpoint(request: ProjectRequest, db: AsyncSession = Depends(get_db)):
    """Get AI-recommended portfolio projects based on skills and goals."""
    try:
        result = await recommend_projects(
            request.goal, request.skills, request.interest, request.difficulty
        )
        await save_history(
            db, "projects",
            f"Projects for {request.goal}",
            f"{len(result.get('projects', []))} project ideas",
            result,
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Project recommendation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


# ─── Learning Planner ──────────────────────────────────────────────────────────

@router.post("/planner", response_model=PlannerResponse)
async def planner_endpoint(request: PlannerRequest, db: AsyncSession = Depends(get_db)):
    """Generate a structured daily learning plan (30/60/90 days)."""
    try:
        result = await generate_planner(
            request.duration, request.hours_per_day, request.goal, request.start_date
        )
        await save_history(
            db, "planner",
            f"{request.duration}-Day Plan — {request.goal}",
            f"{len(result.get('weeks', []))} weeks · {result.get('total_hours', 0)} hours",
            result,
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Planner generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate plan")


# ─── Chat ──────────────────────────────────────────────────────────────────────

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Generate a streaming AI chat response for career guidance."""
    try:
        response = await generate_chat_response(request.message, request.history or [])
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail="Chat service unavailable")


# ─── History ────────────────────────────────────────────────────────────────────

@router.get("/history")
async def history_endpoint(
    feature: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve user history, optionally filtered by feature."""
    records = await get_history(db, feature)
    return [
        {
            "id": r.id,
            "feature": r.feature,
            "title": r.title,
            "summary": r.summary,
            "data": r.data,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]


@router.delete("/history/{record_id}")
async def delete_history_endpoint(record_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a history entry by ID."""
    deleted = await delete_history(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}



email_service = EmailService()


@router.post("/send-registration-email")
async def send_registration_email(request: EmailRequest):

    success = email_service.send_registration_email(
        request.email,
        request.username
    )

    if success:
        return {"message": "Registration email sent"}

    raise HTTPException(status_code=500, detail="Failed to send email")


@router.post("/send-login-email")
async def send_login_email(request: EmailRequest):

    success = email_service.send_login_email(
        request.email,
        request.username
    )

    if success:
        return {"message": "Login email sent"}

    raise HTTPException(status_code=500, detail="Failed to send email")