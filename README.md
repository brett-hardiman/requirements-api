# Requirements Generator API

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Built%20With-FastAPI-009688)](https://fastapi.tiangolo.com)
[![Powered By](https://img.shields.io/badge/Powered%20By-Claude%20Sonnet-1DB954)](https://anthropic.com)

A FastAPI backend that accepts a plain-text project description and returns structured user stories with acceptance criteria — powered by the Anthropic Claude API.

---

## What It Does

Send a plain-English project description to a single POST endpoint. Get back a structured JSON payload containing a project summary and a set of user stories in standard Agile format (As a... I want... So that...), each with acceptance criteria.

This is the API version of a requirements authoring workflow previously done manually or through standalone scripts.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/generate-requirements` | Generate user stories from a project description |
| GET | `/health` | Health check — returns `{"status": "ok"}` |
| GET | `/docs` | Auto-generated Swagger UI (FastAPI built-in) |

---

## Request & Response

**POST `/generate-requirements`**

Request body:
```json
{
  "project_description": "A web app that lets project managers upload a technical doc and get draft user stories back.",
  "num_stories": 5
}
```

`num_stories` is optional and defaults to 5.

Response:
```json
{
  "project_summary": "A document upload tool that auto-generates Agile user stories from technical specifications.",
  "user_stories": [
    {
      "title": "Upload Technical Document",
      "as_a": "project manager",
      "i_want": "to upload a technical specification document",
      "so_that": "the system can analyze it and generate draft user stories automatically",
      "acceptance_criteria": [
        "User can upload a PDF or plain text file up to 10MB",
        "System acknowledges successful upload with a confirmation message",
        "Unsupported file types return a clear error message"
      ]
    }
  ]
}
```

---

## Project Structure

```
requirements-api/
├── main.py              # Entire API — routes, models, logic
├── requirements.txt     # Python dependencies (4 packages)
├── .env                 # Local only — NEVER commit this
├── .env.example         # Committed placeholder — documents required vars
├── .gitignore           # Excludes .env and __pycache__
├── README.md            # This file
└── CLAUDE.md            # Conventions for AI-assisted development
```

---

## Tech Stack

| Technology | Role |
|------------|------|
| Python 3.11+ | Language |
| FastAPI | Web framework + automatic API docs |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |
| Anthropic Python SDK | Claude API client |

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

Open `http://localhost:8000/docs` in your browser. FastAPI generates interactive Swagger UI automatically — no Postman required.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key from console.anthropic.com |

Never commit your `.env` file. The `.gitignore` excludes it by default.

---

## Key Concepts Demonstrated

- **FastAPI routing** — `@app.post()` decorator maps a URL to a Python function
- **Pydantic models** — typed request/response schemas with auto-validation
- **Structured LLM output** — prompting Claude to return only JSON, then parsing and validating it
- **Environment variable management** — API keys via `.env`, never hardcoded
- **HTTP error handling** — `HTTPException` for graceful failure responses
- **Auto-documentation** — Swagger UI generated at `/docs` with zero extra code

---

## What's Next

Planned extensions for v2:
- `GET /requirements/{id}` — retrieve previously generated stories (requires a database)
- `POST /upload` — accept a PDF or `.txt` file as input instead of raw text
- API key authentication on the endpoint itself
- Deploy to Railway or Render (free tier)

---

*Built by Brett Hardiman as part of an AI Engineer skill-building track.*
