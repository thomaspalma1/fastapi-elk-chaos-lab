from pydantic import BaseModel


class MemoryPressureRequest(BaseModel):
    duration_seconds: int = 60
    intensity: float = 0.5


class MemoryPressureResponse(BaseModel):
    scenario: str
    status: str
    duration_seconds: int
