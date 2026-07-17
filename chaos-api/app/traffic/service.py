"""Business logic for traffic endpoints.

This is where active chaos scenarios actually take effect: before
returning a response, each traffic endpoint checks which scenarios are
currently active and applies each of their effects.
"""

from app.scenarios.registry import APPLY_FUNCTIONS
from app.shared import state
from model import OrderResponse


async def process_order() -> OrderResponse:
    active_scenarios = state.get_all_active()

    applied_scenario_names: list[str] = []

    for scenario_name, intensity in active_scenarios.items():
        apply_effect = APPLY_FUNCTIONS[scenario_name]

        await apply_effect(intensity)

        applied_scenario_names.append(scenario_name)

    return OrderResponse(
        status="order_processed",
        applied_scenarios=applied_scenario_names,
    )
