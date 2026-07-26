from fastapi import APIRouter

from app.scenarios.db_timeout.model import DBTimeoutRequest, DBTimeoutResponse
from app.scenarios.db_timeout import service

router = APIRouter(prefix="/simulate/db-timeout", tags=["db-timeout"])


@router.post("", response_model=DBTimeoutResponse)
async def activate_db_timeout(payload: DBTimeoutRequest):
    await service.activate(payload.duration_seconds, payload.intensity)
    return DBTimeoutResponse(
        scenario=service.SCENARIO_NAME,
        status="active",
        duration_seconds=payload.duration_seconds,
    )


@router.delete("", response_model=DBTimeoutResponse)
async def deactivate_db_timeout():
    await service.deactivate()
    return DBTimeoutResponse(
        scenario=service.SCENARIO_NAME,
        status="inactive",
    )
