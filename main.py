from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import os

app = FastAPI(title="Requirements Generator API")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# --- Request & Response Models ---

class RequirementsRequest(BaseModel):
    project_description: str
    num_stories: int = 5  # optional, defaults to 5

class UserStory(BaseModel):
    title: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: list[str]

class RequirementsResponse(BaseModel):
    project_summary: str
    user_stories: list[UserStory]

# --- Endpoint ---

@app.post("/generate-requirements", response_model=RequirementsResponse)
def generate_requirements(request: RequirementsRequest):
    prompt = f"""
You are a senior business analyst and requirements engineer.

Given the following project description, generate exactly {request.num_stories} user stories with acceptance criteria.

Project Description:
{request.project_description}

Respond ONLY with a valid JSON object in this exact format, no markdown, no extra text:
{{
  "project_summary": "One sentence summary of the project",
  "user_stories": [
    {{
      "title": "Short story title",
      "as_a": "type of user",
      "i_want": "goal or feature",
      "so_that": "business value or reason",
      "acceptance_criteria": [
        "Criterion 1",
        "Criterion 2",
        "Criterion 3"
      ]
    }}
  ]
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        raw = message.content[0].text
        data = json.loads(raw)
        return RequirementsResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse model response: {str(e)}")


# --- Health Check ---

@app.get("/health")
def health():
    return {"status": "ok"}
