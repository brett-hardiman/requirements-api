from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(f"Request received: project_description length={len(request.project_description)}, num_stories={request.num_stories}")

    prompt = f"""
You are a senior business analyst and requirements engineer.

Given the following project description, generate up to {request.num_stories} user stories based on the project complexity. Use your judgment to create only as many stories as are appropriate — you may generate fewer if the project is simple.

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

    logger.info("Calling Claude API with model=claude-sonnet-4-20250514")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    logger.info("Claude response received, parsing JSON")
    try:
        raw = message.content[0].text
        data = json.loads(raw)
        response = RequirementsResponse(**data)
        logger.info("Response validated successfully")
        return response
    except Exception as e:
        logger.error(f"Failed to parse Claude response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse model response: {str(e)}")


# --- Health Check ---

@app.get("/health")
def health():
    return {"status": "ok"}
