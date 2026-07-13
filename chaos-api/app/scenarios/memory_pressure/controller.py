from fastapi import APIRouter
from .model import MemoryPressureRequest, MemoryPressureResponse
from .service import *


router = APIRouter(
        prefix="/simulate/memory-pressure", 
        tags=["memory-pressure"]
        )

@router.post("", response_model=MemoryPressureResponse)
async def activate_memory_pressure(payload: MemoryPressureRequest):
    await service.activate(payload.duration_seconds, payload.intensity)
    return MemoryPressureResponse(
        scenario=service.SCENARIO_NAME,
        status="active",
        duration_seconds=payload.duration_seconds,
    )

@router.delete("")
async def deactivate_memory_pressure():
    await service.deactivate()
    return {
            "scenario": service.SCENARIO_NAME, 
            "status": "inactive"
            }
