"""
Central mapping of scenario name to its apply() function.

This is the only place the traffic module needs to know about when
checking which chaos effect to run for each active scenario. Adding a
new scenario means implementing its service module and adding one line
here, nothing else needs to change.
"""

from app.scenarios.db_timeout import service as db_timeout
from app.scenarios.memory_pressure import service as memory_pressure

APPLY_FUNCTIONS = {
    "memory-pressure": memory_pressure.apply,
    "db-timeout": db_timeout.apply,
}
