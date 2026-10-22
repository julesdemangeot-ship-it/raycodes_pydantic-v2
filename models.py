from typing import List

from pydantic import BaseModel, Field, field_validator


class ResearchReport(BaseModel):
    title: str = Field(..., min_length=1, description="A catchy, SEO-friendly title for the report.")
    executive_summary: str = Field(..., min_length=1, description="A short 2-3 sentence summary of the findings.")
    key_findings: List[str] = Field(
        ...,
        min_length=3,
        max_length=5,
        description="A list of 3-5 key findings from the research.",
    )
    conclusion: str = Field(..., min_length=1, description="A concluding paragraph.")

    @field_validator("title", "executive_summary", "conclusion", mode="before")
    @classmethod
    def strip_text(cls, v):
        # Strip whitespace only; keep the model's casing (acronyms like GPT-4, NASA stay intact).
        return v.strip() if isinstance(v, str) else v

    @field_validator("key_findings", mode="before")
    @classmethod
    def clean_findings(cls, v):
        # Runs before the 3-5 length check, so blank entries don't count as findings.
        if isinstance(v, list):
            return [f.strip() for f in v if isinstance(f, str) and f.strip()]
        return v
