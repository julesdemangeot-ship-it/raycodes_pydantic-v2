from pydantic import BaseModel, Field, field_validator
from typing import List

class ResearchReport(BaseModel):
    title: str = Field(..., description="A catchy, SEO-friendly title for the report.")
    executive_summary: str = Field(..., description="A short 2-3 sentence summary of the findings.")
    key_findings: List[str] = Field(..., description="A list of 3-5 key findings from the research.")
    conclusion: str = Field(..., description="A concluding paragraph.")

    @field_validator("title")
    @classmethod
    def clean_title(cls, v: str) -> str:
        # Pydantic v2 validator to ensure title is title-cased and stripped
        return v.strip().title()

    @field_validator("key_findings")
    @classmethod
    def validate_findings(cls, v: List[str]) -> List[str]:
        # Ensure we have at least 1 finding
        if not v:
            raise ValueError("Must have at least one key finding")
        return [finding.strip() for finding in v if finding.strip()]
