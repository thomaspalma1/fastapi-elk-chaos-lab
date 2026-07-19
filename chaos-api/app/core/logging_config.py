"""
Structured JSON logging configuration for the chaos API.

Every log record includes a "log_type" field, used by the Logstash
pipeline to route logs to the correct Elasticsearch index:
  - "app-log": regular traffic/scenario-effect logs -> app-logs-*
  - "chaos-event": scenario activation/deactivation  -> chaos-events-*
"""

import logging
from pythonjsonlogger.json import JsonFormatter


def configure_logging() -> None:
    """Configure the "app" logger to emit structured JSON to stdout."""
    handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "@timestamp", "levelname": "level"},
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
