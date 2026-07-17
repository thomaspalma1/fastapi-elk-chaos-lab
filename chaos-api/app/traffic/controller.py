from fastapi import APIRouter

from app.traffic import service
from app.traffic.model import OrderResponse

router = APIRouter(tags=["traffic"])


@router.post("/orders", response_model=OrderResponse)
async def create_order() -> OrderResponse:
    return await service.process_order()
