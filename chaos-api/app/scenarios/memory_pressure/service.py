import random
import logging
from app.shared import state

logger = logging.getLogger("app")

SCENARIO_NAME = "memory-pressure"
ALLOCATION_SIZE = 10000000  # Number of allocated elements per occurrence


async def activate(duration_seconds: int, intensity: float):
    state.set_active(SCENARIO_NAME, duration_seconds, intensity)
    logger.info(
        "scenario_activated",
        extra={
            "scenario": SCENARIO_NAME,
            "duration_seconds": duration_seconds,
            "intensity": intensity,
        },
    )


async def deactivate():
    state.remove_active(SCENARIO_NAME)
    logger.info("scenario_deactivated", extra={"scenario": SCENARIO_NAME})


async def apply(intensity: float):
    if random.random() < intensity:
        _ = [0] * ALLOCATION_SIZE
        logger.warning(
            "memory_pressure",
            extra={"scenario": SCENARIO_NAME, "memory_usage_mb": 80},
        )
