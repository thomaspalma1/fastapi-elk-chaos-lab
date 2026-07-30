"""Business logic for the db-timeout chaos scenario.

Simulates a database query that doesn't return within the expected
time, by adding an artificial delay to a percentage of traffic requests
while the scenario is active. The scenario is persistent: it stays
active until explicitly deactivated.
"""

import asyncio
import random

from loguru import logger

from app.shared import state

SCENARIO_NAME = "db-timeout"
MIN_DELAY_SECONDS = 2
MAX_DELAY_SECONDS = 5


async def activate(intensity: float) -> None:
    """Mark this scenario as active with the given intensity."""
    state.set_active(SCENARIO_NAME, intensity)
    logger.bind(
        log_type="chaos-event",
        scenario=SCENARIO_NAME,
        intensity=intensity,
    ).info("scenario_activated")


async def deactivate() -> None:
    """Deactivate the scenario."""
    state.remove_active(SCENARIO_NAME)
    logger.bind(
        log_type="chaos-event",
        scenario=SCENARIO_NAME,
    ).info("scenario_deactivated")


async def apply(intensity: float) -> None:
    """Apply the db-timeout effect for a single traffic request.

    With probability equal to `intensity`, waits for a random delay
    (simulating a slow/timed-out query) and logs the real time spent.
    """
    if random.random() >= intensity:
        return

    delay_seconds = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
    await asyncio.sleep(delay_seconds)

    logger.bind(
        log_type="app-log",
        scenario=SCENARIO_NAME,
        db_query_time_ms=round(delay_seconds * 1000, 2),
        db_status="timeout",
    ).warning("db_query_timeout")
