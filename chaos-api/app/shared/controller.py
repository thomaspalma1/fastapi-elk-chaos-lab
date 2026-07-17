"""
Shared endpoint for querying scenario status.
Exposes a single read-only endpoint that lets clients confirm which
chaos scenarios are currently active, without relying only on log
inspection.
"""

from fastapi import APIRouter
from app.shared import state

router = APIRouter (prefix="/simulate", tags=["status"])

@router.get("/status")
async def get_active_scenarios() -> dict:
    """Return every scenario currently active, with its intensity."""
    return {"active_scenarios": state.get_all_active()}
