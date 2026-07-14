from pydantic import BaseModel, Field


class MemoryPressureRequest(BaseModel):
    duration_seconds: int = Field(
        default=60, gt=0, description="How long the scenario stays active"
    )
    intensity: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Percentage of requests affected"
    )


class MemoryPressureResponse(BaseModel):
    scenario: str
    status: str
    duration_seconds: int | None = None
