"""
CareerPilot AI — FastAPI Application Entry Point

Configures the FastAPI application with:
- CORS middleware
- Rate limiting
- Database initialization
- API routes
- Health check endpoint
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info("CareerPilot AI backend starting up...")
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("CareerPilot AI backend shutting down...")


app = FastAPI(
    title="CareerPilot AI",
    description="AI-powered career mentor for placement preparation",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Client-Info", "Apikey"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["CareerPilot AI"])


@app.get("/")
async def root():
    """Root health check endpoint."""
    return {
        "name": "CareerPilot AI",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint for load balancers / monitoring."""
    return {"status": "healthy", "service": "careerpilot-ai"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )
