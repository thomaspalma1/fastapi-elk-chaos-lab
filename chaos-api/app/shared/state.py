"""In-memory state store for chaos scenarios.

This module exists because scenario activation (POST /simulate/{name}) and
scenario application (e.g. POST /orders) happen in two separate HTTP
requests with no direct connection between them. Something needs to hold
"which scenarios are active right now" so the traffic endpoints can check
it before applying any chaos effect.

Scenarios are persistent by design: once activated, a scenario stays
active until explicitly deactivated via DELETE /simulate/{name}. There is
no automatic expiration — this mirrors real incidents, which persist
until someone intervenes, and avoids a scenario silently turning off
mid-investigation.

It intentionally knows nothing about individual scenarios (no memory
pressure, no db timeout, etc.) — it only understands the generic concept
of "a named scenario is active, with some intensity".
"""

_active_scenarios: dict[str, float] = {}


def set_active(name: str, intensity: float) -> None:
    """Register a scenario as active, with the given intensity.

    Args:
        name: Unique identifier of the scenario (e.g. "db-timeout").
        intensity: Percentage of requests affected, between 0.0 and 1.0.

    Returns:
        None.
    """
    _active_scenarios[name] = intensity


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

    Returns:
        A mapping of scenario name to intensity.
    """
    return dict(_active_scenarios)
