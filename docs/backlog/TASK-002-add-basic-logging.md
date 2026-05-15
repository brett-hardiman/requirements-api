# TASK-002: Add Basic Logging

## Phase
Phase 1 - v1 Completion

## Description
The current main.py has no observability. Per the project plan (section 11), add Python's built-in `logging` module to track key events: request received, Claude API call initiated, response received, and parse success/failure. This provides visibility when running locally and debugging issues.

## Dependencies
NONE

## Acceptance Criteria

- Given main.py, when logging is configured, then `logging.basicConfig(level=logging.INFO)` and `logger = logging.getLogger(__name__)` are set up at module level (near the top of the file, after imports)
- Given the `/generate-requirements` endpoint, when a request is received, then log: "Request received: project_description length={len}, num_stories={n}"
- Given the endpoint executes a Claude API call, when the call is initiated, then log: "Calling Claude API with model=claude-sonnet-4-20250514"
- Given the Claude API returns a response, when the response is received, then log: "Claude response received, parsing JSON"
- Given the JSON parsing succeeds, when the response is validated, then log: "Response validated successfully"
- Given the JSON parsing fails, when the exception is caught, then log: "Failed to parse Claude response: {error}" at ERROR level before raising HTTPException
- Given all logging statements are added, when tested via `/docs`, then logs appear in the uvicorn console output with INFO level visibility

## Technical Notes
- Add `import logging` at the top of main.py (move the existing `import json` from line 64 to the top as well, per project plan section 15)
- Configure logging after imports and before FastAPI app instantiation
- Use `logger.info()` for normal flow and `logger.error()` for exception cases
- Do NOT use print statements (per CLAUDE.md review standards: "No secrets, hardcoded values, or print statements in committed code")
- Keep log messages concise and structured; avoid logging sensitive data
- The project plan lists four key log points: request received, Claude call initiated, response received, parse outcome

## Estimated Complexity
S
