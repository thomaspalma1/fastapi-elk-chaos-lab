"""Central mapping of scenario name to its apply() function.

This is the only place the traffic module needs to know about when
checking which chaos effect to run for each active scenario. Adding a
new scenario means implementing its service module and adding one line
here, nothing else needs to change.
"""

from app.scenarios.memory_pressure import service as memory_pressure

APPLY_FUNCTIONS = {
    "memory-pressure": memory_pressure.apply,
}

# As new scenarios are implemented (db_timeout, cache_down, payment_timeout,
# etc.), import their service module above and register their apply()
# function in this dict following the same pattern.
