# CareerPilot AI — Backend

FastAPI backend for the CareerPilot AI application.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker

```bash
docker build -t careerpilot-backend .
docker run -p 8000:8000 --env-file .env careerpilot-backend
```

Or with Docker Compose (from project root):
```bash
docker-compose up --build
```
