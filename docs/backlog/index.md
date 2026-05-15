# Backlog Index

| ID | Title | Phase | Dependencies | Complexity | Status |
|----|-------|-------|--------------|------------|--------|
| TASK-001 | Update Prompt to Treat num_stories as Maximum | Phase 1 - v1 Completion | NONE | S | PENDING |
| TASK-002 | Add Basic Logging | Phase 1 - v1 Completion | NONE | S | PENDING |

---

## Execution Notes

Both tasks are independently executable with no dependencies. Recommended order:

1. TASK-001 (prompt update) - Functional change, easier to validate in isolation
2. TASK-002 (logging) - Observability enhancement, easier to verify if logs show both old and new prompt behavior

Alternatively, they can be executed in parallel or reversed order without issues.

---

## Out of Scope (Phase 2+)

- Railway deployment
- API key authentication
- Rate limiting
- PDF upload endpoint
- Pytest test suite
- Streaming responses
- Improved error distinction (network vs parse)
