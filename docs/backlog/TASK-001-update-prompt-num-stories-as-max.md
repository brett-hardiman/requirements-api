# TASK-001: Update Prompt to Treat num_stories as Maximum

## Phase
Phase 1 - v1 Completion

## Description
The current prompt instructs Claude to generate exactly `num_stories` user stories. Per the project plan (section 6), `num_stories` should be treated as a maximum, allowing Claude to generate fewer stories if the project complexity doesn't warrant the full count. This gives Claude discretion to avoid padding with low-quality stories.

## Dependencies
NONE

## Acceptance Criteria

- Given the `/generate-requirements` endpoint in main.py, when the prompt text is updated, then it changes from "generate exactly {request.num_stories}" to "generate up to {request.num_stories}" or equivalent phrasing that treats num_stories as a maximum
- Given the updated prompt, when a request is submitted with `num_stories=5` and a simple project description, then Claude may return fewer than 5 stories if appropriate
- Given the prompt update, when manually tested via `/docs`, then the response still validates against the `RequirementsResponse` Pydantic model with no errors

## Technical Notes
- The prompt is located in the `generate_requirements()` function in main.py (lines 31-56)
- The exact line to modify is line 34: "generate exactly {request.num_stories} user stories"
- Suggested replacement: "generate up to {request.num_stories} user stories based on the project complexity"
- Do NOT modify the JSON schema structure or any Pydantic models
- Do NOT add new validation logic; this is purely a prompt text change

## Estimated Complexity
S
