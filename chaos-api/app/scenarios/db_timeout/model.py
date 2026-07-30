from pydantic import BaseModel, Field


class DBTimeoutRequest(BaseModel):
    intensity: float = Field(
        default=0.5, ge=0.0, le=1.0, 
        description="Percentage of requests affected")


class DBTimeoutResponse(BaseModel):
    scenario: str
    status: str
