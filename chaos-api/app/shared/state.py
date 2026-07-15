import time

_active_scenarios: dict[str, dict] = {}


def set_active(name: str, duration_seconds: int, intensity: float) -> None:
    _active_scenarios[name] = {
        "intensity": intensity,
        "expires_at": time.time() + duration_seconds,
    }


def remove_active(name: str) -> None:
    _active_scenarios.pop(name, None)


def get_all_active() -> dict[str, float]:
    now = time.time()
    expired = [name for name, data in _active_scenarios.items() if data["expires_at"] <= now]
    for name in expired:
        del _active_scenarios[name]
    return {name: data["intensity"] for name, data in _active_scenarios.items()}
