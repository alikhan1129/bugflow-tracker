from typing import Optional
from pydantic import BaseModel, Field, field_validator

class BugCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    use_ai_triage: bool = False

class BugUpdate(BaseModel):
    status: Optional[str] = None
    resolution_notes: Optional[str] = None

class AITriageResponse(BaseModel):
    severity: str
    category: str
    title: str

    @field_validator('severity')
    def validate_severity(cls, v):
        v = v.lower()
        if v not in ['low', 'medium', 'high']: return 'medium'
        return v

    @field_validator('category')
    def validate_category(cls, v):
        # The proj detaiils.txt says UI|backend|performance (case insensitive based on example)
        v = v.lower()
        if v not in ['ui', 'backend', 'performance']: return 'backend'
        return v
