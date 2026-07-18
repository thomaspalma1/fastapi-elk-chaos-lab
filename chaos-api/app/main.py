from fastapi import FastAPI
from app.scenarios.memory_pressure.controller import router
from app.shared.controller import router as status_router
from app.traffic.controller import router as traffic_router


app = FastAPI(
    title="Observability Chaos Lab with FastAPI",
    summary="Chaos engineering API for generating observability scenarios.",
    version="0.1.0",
    description=(
        "This application acts as a chaos orchestrator, generating various scenarios "
        "and events that produce structured logs. These logs are collected and analyzed "
        "using the ELK Stack (Elasticsearch, Logstash, and Kibana). The goal is to create "
        "a controlled environment for exploring log aggregation, search, visualization, "
        "and operational monitoring."
    ),
)

app.include_router(router)
app.include_router(status_router)
app.include_router(traffic_router)
