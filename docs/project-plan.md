# Requirements Generator API - Technical Blueprint

Version: 1.0
Date: 2026-05-15
Status: Active

---

## 1. Project Overview

### Goal
A FastAPI backend that accepts a plain-text project description and returns structured Agile user stories with acceptance criteria, powered by the Anthropic Claude API.

### Non-Goals (v1)
- No database or persistence
- No authentication or authorization
- No rate limiting or cost controls
- No retries on failure
- No automated tests (pytest)
- No batching or streaming responses
- No PDF upload
- No deployment to cloud infrastructure

### User Persona
Solo developer using the API locally via terminal (curl) or Swagger UI. Input is typically 2-5 sentences describing a project idea.

---

## 2. Tech Stack

| Technology | Version | Justification |
|------------|---------|---------------|
| Python | 3.11+ | Required by CLAUDE.md; modern type hints and performance |
| FastAPI | latest | Required by CLAUDE.md; async-ready, auto-generated OpenAPI docs |
| Pydantic | v2 | Required by CLAUDE.md; request/response validation |
| Anthropic SDK | latest | Official Python client for Claude API |
| Uvicorn | latest | ASGI server for FastAPI |

---

## 3. File Structure

```
requirements-api/
├── main.py              # Entire API: routes, models, Claude calls
├── requirements.txt     # Python dependencies (minimal)
├── .env                 # Local secrets (never committed)
├── .env.example         # Placeholder for required env vars
├── .gitignore           # Excludes .env and __pycache__
├── README.md            # Human documentation
├── CLAUDE.md            # AI development conventions
└── docs/
    └── project-plan.md  # This file
```

All application code lives in `main.py`. This is a deliberate v1 constraint per CLAUDE.md: "single-file API with no database."

---

## 4. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Python variables | snake_case | `project_description` |
| Python functions | snake_case | `generate_requirements` |
| Pydantic models | PascalCase | `RequirementsRequest` |
| URL paths | kebab-case | `/generate-requirements` |
| Env vars | SCREAMING_SNAKE | `ANTHROPIC_API_KEY` |
| Git branches | feature/short-description | `feature/add-pdf-upload` |
| Git commits | feat(scope): message | `feat(api): add health check` |

---

## 5. API Surface

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/generate-requirements` | Generate user stories from project description |
| GET | `/health` | Health check for monitoring |
| GET | `/docs` | Swagger UI (auto-generated) |
| GET | `/openapi.json` | OpenAPI spec (auto-generated) |

### Request Model: `RequirementsRequest`

```python
class RequirementsRequest(BaseModel):
    project_description: str  # Plain text, 2-5 sentences typical
    num_stories: int = 5      # Maximum stories to generate (not exact)
```

### Response Models

```python
class UserStory(BaseModel):
    title: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: list[str]

class RequirementsResponse(BaseModel):
    project_summary: str
    user_stories: list[UserStory]
```

### Example Request

```json
{
  "project_description": "A mobile app that lets users track their daily water intake and sends reminders to stay hydrated.",
  "num_stories": 5
}
```

### Example Response

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

## 6. Prompt Engineering Approach

### Constraints from CLAUDE.md
1. Instruct Claude to return **only valid JSON** - no markdown, no preamble, no backticks
2. System prompt lives in user message (v1 simplicity)
3. Model: `claude-sonnet-4-20250514` (hardcoded per CLAUDE.md)
4. `max_tokens`: 2048 (capped per human decision)

### Current Prompt Structure

The prompt in `main.py` instructs Claude to act as a senior business analyst and return a JSON object matching `RequirementsResponse` exactly. Key elements:

- Role assignment: "senior business analyst and requirements engineer"
- Explicit JSON schema in prompt
- "Respond ONLY with valid JSON" instruction
- No markdown/extra text warning

### Required Prompt Update

The current prompt says "generate exactly {num_stories}" but human decision specifies `num_stories` is a **maximum**, not exact. The prompt should be updated to:

```
Generate UP TO {request.num_stories} user stories based on the project complexity.
```

---

## 7. Error and Validation Strategy

### Validation Flow
1. FastAPI/Pydantic validates incoming request against `RequirementsRequest`
2. Claude API called with structured prompt
3. Response text parsed with `json.loads()`
4. Parsed dict validated against `RequirementsResponse` Pydantic model
5. Validated response returned to client

### Error Handling Rules (per CLAUDE.md)
- All exceptions wrapped in `HTTPException` with descriptive `detail`
- Raw exceptions never surface to caller
- No retries on failure (v1 decision)

### Error Scenarios

| Scenario | HTTP Status | Detail Message |
|----------|-------------|----------------|
| Invalid request body | 422 | Pydantic validation error (auto) |
| Missing ANTHROPIC_API_KEY | 500 | Environment variable not set |
| Anthropic API unreachable | 500 | "Failed to parse model response: {error}" |
| Claude returns invalid JSON | 500 | "Failed to parse model response: {error}" |
| Pydantic validation of response fails | 500 | "Failed to parse model response: {error}" |

Note: Current implementation catches all exceptions in one block. This is acceptable for v1 simplicity but could be refined in v2 to distinguish network errors from parse errors.

---

## 8. Environment and Configuration

### Required Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| ANTHROPIC_API_KEY | Authenticate with Anthropic API | sk-ant-xxx |

### .env.example (current)
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Loading Convention
```python
os.environ.get("ANTHROPIC_API_KEY")
```

Per CLAUDE.md: Never hardcode API keys. All secrets via environment variables.

---

## 9. Testing Approach

### v1: Swagger UI Only
- All endpoints tested manually via `/docs`
- Verify response shape matches Pydantic model
- Test edge cases: empty description, large num_stories, special characters

### Test Checklist for `/generate-requirements`
- [ ] Valid request returns 200 with correct structure
- [ ] Empty `project_description` handled gracefully
- [ ] `num_stories=1` works
- [ ] `num_stories=20` works (large but valid)
- [ ] Invalid JSON in request body returns 422

### v2: Pytest
Deferred until more endpoints exist. Will include:
- Unit tests for Pydantic models
- Integration tests with mocked Anthropic client
- Contract tests for response shape

---

## 10. Deployment Plan

### v1: Local Only
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
cp .env.example .env
# Edit .env with real ANTHROPIC_API_KEY

# Run server
uvicorn main:app --reload
```

Access at: http://localhost:8000/docs

### v2: Railway Free Tier
- Configure `ANTHROPIC_API_KEY` as Railway secret
- Add Procfile or railway.json for deployment
- No hardcoded localhost references (already compliant)
- All paths relative or environment-configurable

---

## 11. Observability

### v1: Basic Logging
- Python `logging` module or print statements
- Log: incoming requests, Claude API calls, errors
- No external services (Sentry, Datadog)

### Current State
The existing `main.py` has no logging. This should be added:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

Log points:
- Request received (project_description length, num_stories)
- Claude API call initiated
- Claude API response received (token count if available)
- Parse success/failure

---

## 12. Security Posture

### v1 Constraints
- No authentication (internal/localhost only)
- No rate limiting
- No input sanitization beyond Pydantic validation

### Hardening Already in Place
- API key loaded from environment, not hardcoded
- `.env` excluded from git
- No hardcoded localhost URLs in code

### v2 Security Additions
- API key authentication for public deployment
- Rate limiting per API key
- Input length validation (prevent prompt injection via very long inputs)

---

## 13. Phased Roadmap

### Phase 1: v1 Current State (Complete)
- [x] Single-file FastAPI application
- [x] `/generate-requirements` endpoint
- [x] `/health` endpoint
- [x] Pydantic request/response validation
- [x] Claude API integration
- [x] Environment variable configuration
- [ ] Update prompt to treat `num_stories` as maximum (minor fix)
- [ ] Add basic logging

### Phase 2: v2 Public Deployment
- [ ] Deploy to Railway free tier
- [ ] Add API key authentication (header-based)
- [ ] Add rate limiting (per API key)
- [ ] Add pytest test suite
- [ ] Improve error messages (distinguish network vs parse errors)

### Phase 3: v2 PDF Upload
- [ ] Add `/upload-pdf` endpoint
- [ ] PDF text extraction (PyPDF2 or pdfplumber)
- [ ] Chunking strategy for large documents
- [ ] Update prompt to handle extracted text

### Phase 4: Nice-to-Haves (Unscheduled)
- Streaming responses (Server-Sent Events)
- Batch processing multiple descriptions
- Story prioritization and dependencies
- Export to Jira/Linear format

---

## 14. Open Questions

None. All decisions made by human during discovery.

---

## 15. Appendix: Current main.py Analysis

The existing scaffold is compliant with CLAUDE.md conventions:

| Convention | Status |
|------------|--------|
| Python 3.11+ syntax | Compliant (list[str] type hints) |
| Pydantic v2 BaseModel | Compliant |
| PascalCase models | Compliant |
| snake_case functions | Compliant |
| kebab-case URLs | Compliant |
| HTTPException for errors | Compliant |
| claude-sonnet-4-20250514 model | Compliant |
| JSON-only prompt instruction | Compliant |
| json.loads in try/except | Compliant |
| Pydantic response validation | Compliant |
| No hardcoded API keys | Compliant |

### Minor Updates Needed
1. Prompt text: Change "exactly" to "up to" for `num_stories`
2. Add logging statements
3. Move `import json` to top of file (style)

These are refinements, not architectural changes. The scaffold is production-ready for v1 scope.
