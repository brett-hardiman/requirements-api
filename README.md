# Requirements Generator API

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Built%20With-FastAPI-009688)](https://fastapi.tiangolo.com)
[![Powered By](https://img.shields.io/badge/Powered%20By-Claude%20Sonnet-1DB954)](https://anthropic.com)

---

## What It Is

A FastAPI backend that turns plain-English project descriptions into structured Agile user stories. You send a few sentences describing what you want to build, and the API returns a set of user stories in standard format (As a... I want... So that...), each with acceptance criteria. It's powered by Claude, Anthropic's large language model.

---

## How It Works

You send a POST request with a project description and an optional number of stories you want. The API wraps your input in a structured prompt and sends it to Claude Sonnet 4. Claude analyzes the description and generates user stories based on the project's complexity — it may return fewer stories than requested if the project is simple. The response is parsed, validated against a strict schema, and returned as JSON.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/generate-requirements` | Generate user stories from a project description |
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| GET | `/docs` | Auto-generated Swagger UI (FastAPI built-in) |

---

## Example Request & Response

**POST `/generate-requirements`**

Request body:
```json
{
  "project_description": "A mobile app that lets users track their daily water intake and sends reminders to stay hydrated.",
  "num_stories": 5
}
```

`num_stories` is optional and defaults to 5. The API treats this as a maximum — it may return fewer stories for simple projects.

Response (truncated to one story for brevity):
```json
{
  "project_summary": "A hydration tracking mobile application with reminder functionality.",
  "user_stories": [
    {
      "title": "Log Water Intake",
      "as_a": "health-conscious user",
      "i_want": "to log each glass of water I drink",
      "so_that": "I can track my daily hydration progress",
      "acceptance_criteria": [
        "User can add a water entry with one tap",
        "Entry records timestamp and amount in ml or oz",
        "Daily total updates immediately after logging"
      ]
    }
  ]
}
```

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/brett-hardiman/requirements-api.git
cd requirements-api
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your environment**
```bash
cp .env.example .env
# Open .env and add your Anthropic API key
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Test it**

Open `http://localhost:8000/docs` in your browser. FastAPI generates interactive Swagger UI automatically.

---

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key. Get one at [console.anthropic.com](https://console.anthropic.com/) |

The `.env` file is excluded from version control by default. Never commit it.

---

## Project Status & Roadmap

**Current Status:** v1 complete (local-only deployment)

Phase 1 is finished: the API generates intelligent user stories and logs all key events for debugging.

**Planned for v2:**
- Deploy to Railway or Render (free tier)
- Add API key authentication for public endpoints
- Add PDF upload endpoint — extract text from documents and generate stories from them
- Add rate limiting to prevent abuse
- Add automated test suite (pytest)

---

## Project Layout

```
requirements-api/
├── main.py              # Entire API — routes, models, Claude API calls
├── requirements.txt     # Python dependencies (fastapi, uvicorn, anthropic, pydantic)
├── .env                 # Local secrets — NEVER commit this
├── .env.example         # Placeholder for required environment variables
├── .gitignore           # Excludes .env and __pycache__
├── README.md            # This file
├── CLAUDE.md            # Development conventions (for contributors)
└── docs/                # Project plan and task logs
```

All application code lives in `main.py`. This is a deliberate v1 constraint: single-file API with no database.

---

## Tech Stack

| Technology | Role | Why It Was Chosen |
|------------|------|-------------------|
| Python 3.11+ | Language | Modern type hints and async support |
| FastAPI | Web framework | Auto-generated API docs, async-ready, built-in validation |
| Pydantic v2 | Request/response validation | Strict schema enforcement with helpful error messages |
| Uvicorn | ASGI server | Production-ready server for FastAPI |
| Anthropic Python SDK | Claude API client | Official client for Claude, handles authentication and retries |

---

*Built by Brett Hardiman as part of an AI Engineer skill-building track.*
