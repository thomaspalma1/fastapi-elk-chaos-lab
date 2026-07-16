"""Business logic for the memory-pressure chaos scenario.

Simulates the effect of a system running under memory pressure; e.g. a
memory leak or an oversized in-memory cache by allocating real memory
on each apply() call while the scenario is active, and releasing it all
on deactivate().
"""

import logging
import random

import psutil

from app.shared import state

logger = logging.getLogger("app")

SCENARIO_NAME = "memory-pressure"
BLOCK_SIZE_ELEMENTS = 10000000  # elements allocated per apply() call

# Memory blocks accumulate here while the scenario is active, so the
# pressure effect is cumulative across requests instead of vanishing
# right after each call. Cleared on deactivate().
_allocated_memory_blocks: list[list[int]] = []


async def activate(duration_seconds: int, intensity: float) -> None:
    """Mark this scenario as active for the given duration and intensity."""
    state.set_active(SCENARIO_NAME, duration_seconds, intensity)
    logger.info(
        "scenario_activated",
        extra={
            "log_type": "chaos-event",
            "scenario": SCENARIO_NAME,
            "duration_seconds": duration_seconds,
            "intensity": intensity,
        },
    )


async def deactivate() -> None:
    """Deactivate the scenario and release all memory allocated by it."""
    state.remove_active(SCENARIO_NAME)
    released_block_count = len(_allocated_memory_blocks)
    _allocated_memory_blocks.clear()
    logger.info(
        "scenario_deactivated",
        extra={
            "log_type": "chaos-event",
            "scenario": SCENARIO_NAME,
            "released_block_count": released_block_count,
        },
    )


async def apply(intensity: float) -> None:
    """Apply the memory-pressure effect for a single traffic request.

    With probability equal to `intensity`, allocates one more memory
    block and keeps it referenced (so it isn't garbage collected),
    then logs the real memory delta caused by that allocation.
    """
    if random.random() >= intensity:
        return

    process = psutil.Process()
    memory_before_mb = process.memory_info().rss / (1024 * 1024)

    _allocated_memory_blocks.append([0] * BLOCK_SIZE_ELEMENTS)

    memory_after_mb = process.memory_info().rss / (1024 * 1024)

    logger.warning(
        "memory_pressure_applied",
        extra={
            "log_type": "app-log",
            "scenario": SCENARIO_NAME,
            "memory_usage_delta_mb": round(memory_after_mb - memory_before_mb, 2),
            "total_allocated_blocks": len(_allocated_memory_blocks),
        },
        )
