from fastapi import APIRouter
from .model import MemoryPressureRequest, MemoryPressureResponse

router = APIRouter(
        prefix="/simulate/memory-pressure", 
        tags=["memory-pressure"]
        )

@router.post("", response_model=MemoryPressureResponse)
async def activate_memory_pressure(payload: MemoryPressureRequest):
    pass
