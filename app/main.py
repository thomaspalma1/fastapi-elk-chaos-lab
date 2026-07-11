from fastapi import FastAPI

app = FastAPI(
    title="Observability chaos lab with FastAPI",
    version="0.1.0",
    description=(
        "The application simulates a chaos orchestrator by generating different "
        "scenarios and events that produce structured logs, which are then "
        "collected and analyzed through the ELK Stack (Elasticsearch, Logstash, "
        "and Kibana). Its purpose is to provide a controlled environment for "
        "exploring log aggregation, search, visualization, and operational "
        "monitoring."
    ),
)

