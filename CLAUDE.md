# Project Conventions

## Project Overview

This is a FastAPI backend that wraps the Anthropic Claude API to generate structured Agile user stories from plain-text project descriptions. It is a single-file API with no database (v1).

---

## File Structure

- `main.py` — The entire API. Routes, Pydantic models, and Claude API calls live here.
- `requirements.txt` — Python dependencies. Keep this minimal.
- `.env` — Local secrets. Never committed.
- `.env.example` — Committed placeholder documenting all required env vars with fake values.
- `README.md` — Human-readable project documentation.
- `CLAUDE.md` — This file. Conventions for AI-assisted development.

---

## Code Conventions

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Validation:** Pydantic v2 BaseModel for all request and response shapes
- **Naming:** snake_case for variables, functions, and file names
- **Model naming:** PascalCase for Pydantic models (e.g. `RequirementsRequest`, `UserStory`)
- **Endpoint naming:** kebab-case URL paths (e.g. `/generate-requirements`)
- **Error handling:** Always use `HTTPException` with descriptive `detail` messages — never let raw exceptions surface to the caller
- **Claude model:** Always use `claude-sonnet-4-20250514` unless explicitly updated in this file

---

## Environment Variables

- All secrets and API keys MUST use environment variables loaded via `os.environ.get()`
- Document every required env var in `.env.example` with a placeholder value
- NEVER hardcode API keys, tokens, or environment-specific URLs
- `.env` is excluded from git via `.gitignore`

---

## Anthropic API Conventions

- Always instruct Claude to return only valid JSON — no markdown, no preamble, no backticks
- Always wrap `json.loads()` in a try/except and raise `HTTPException(status_code=500)` on parse failure
- Always validate parsed JSON through the Pydantic response model before returning it
- Keep system prompts in the user message for simplicity (v1) — move to `system=` parameter if prompt complexity grows

---

## Git Conventions

- Branch naming: `feature/[short-description]` (e.g. `feature/add-pdf-upload`)
- Commit format: `feat(scope): description` (e.g. `feat(api): add health check endpoint`)
- No direct pushes to main — use pull requests

---

## Review Standards

- All endpoints must have a corresponding test in the Swagger UI (`/docs`) before being marked complete
- Response shapes must exactly match the declared Pydantic response model
- No secrets, hardcoded values, or print statements in committed code

---

## Deployment Target (v2)

- Railway or Render (free tier)
- All paths and URLs must be relative or environment-configurable
- No hardcoded `localhost` references in committed code
