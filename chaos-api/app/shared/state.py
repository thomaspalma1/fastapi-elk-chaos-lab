"""In-memory state store for chaos scenarios.

This module exists because scenario activation (POST /simulate/{name}) and
scenario application (e.g. POST /orders) happen in two separate HTTP
requests with no direct connection between them. Something needs to hold
"which scenarios are active right now" so the traffic endpoints can check
it before applying any chaos effect.

It intentionally knows nothing about individual scenarios (no memory
pressure, no db timeout, etc.) — it only understands the generic concept
of "a named scenario is active, with some intensity, until some time".
"""

import time

# Private module-level dict: holds the currently active scenarios in memory.
# Not meant to be accessed directly from outside this module — always go
# through set_active / remove_active / get_all_active so expiration and
# access rules stay consistent in one place.
_active_scenarios: dict[str, dict] = {}


def set_active(name: str, duration_seconds: int, intensity: float) -> None:
    """Register a scenario as active.

    Stores the scenario's intensity and computes the timestamp at which
    it should automatically expire.

    Args:
        name: Unique identifier of the scenario (e.g. "memory-pressure").
        duration_seconds: How long the scenario should remain active.
        intensity: Percentage of requests affected, between 0.0 and 1.0.

    Returns:
        None.
    """
    _active_scenarios[name] = {
        "intensity": intensity,
        "expires_at": time.time() + duration_seconds,
    }


def remove_active(name: str) -> None:
    """Manually deactivate a scenario.

    Typically called from a DELETE /simulate/{name} request. Safe to call
    even if the scenario is not currently active.

    Args:
        name: Unique identifier of the scenario to deactivate.

    Returns:
        None.
    """
    _active_scenarios.pop(name, None)


def get_all_active() -> dict[str, float]:
    """Return all currently active scenarios.

    Scenarios past their expiration time are removed as part of this
    call, so every read of the state is guaranteed to be up to date.

    Returns:
        A mapping of scenario name to intensity, containing only
        scenarios that are still active.
    """
    now = time.time()
    expired = [name for name, data in _active_scenarios.items() if data["expires_at"] <= now]
    for name in expired:
        del _active_scenarios[name]
    return {name: data["intensity"] for name, data in _active_scenarios.items()}
