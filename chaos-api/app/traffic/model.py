from pydantic import BaseModel


class OrderResponse(BaseModel):
    status: str
    applied_scenarios: list[str]
