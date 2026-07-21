"""
Structured JSON logging configuration for the chaos API, using Loguru.

Every log record includes a "log_type" field, used by the Logstash
pipeline to route logs to the correct Elasticsearch index:
  - "app-log": regular traffic/scenario-effect logs -> app-logs-*
  - "chaos-event": scenario activation/deactivation  -> chaos-events-*

Loguru's built-in serialize=True produces a nested JSON structure
(fields live under record["extra"]), which doesn't match the flat
fields our Logstash pipeline expects (e.g. log_type at the root of the
document). This custom sink flattens the record manually instead.
"""

import json
import sys

from loguru import logger


def json_sink(message) -> None:
    """Write a single Loguru record as a flat JSON line to stderr."""
    record = message.record

    log_entry = {
        "@timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "level": record["level"].name,
        "name": "app",
        "message": record["message"],
    }
    # Fields passed via logger.bind(...) land in record["extra"];
    # merge them at the root so log_type, scenario, etc. are top-level.
    log_entry.update(record["extra"])

    print(json.dumps(log_entry), file=sys.stderr)


def configure_logging() -> None:
    """Configure Loguru to emit structured JSON to stderr."""
    logger.remove()  # removes Loguru's default colored console sink
    logger.add(json_sink, level="INFO")
