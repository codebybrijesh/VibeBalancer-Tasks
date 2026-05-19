from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response
import httpx
import asyncio
import psutil

from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = FastAPI()

servers = [
    "http://localhost:8001",
    "http://localhost:8002"
]
# LOAD BALANCER STATE
current = 0

connections = {
    "http://localhost:8001": 0,
    "http://localhost:8002": 0
}

server_health = {
    "http://localhost:8001": True,
    "http://localhost:8002": True
}

strategy = "round_robin"

# PROMETHEUS METRICS

REQUEST_COUNT = Counter(
    "load_balancer_requests_total",
    "Total requests received"
)

ERROR_COUNT = Counter(
    "load_balancer_errors_total",
    "Total failed requests"
)

ACTIVE_CONNECTIONS = Gauge(
    "load_balancer_active_connections",
    "Current active connections"
)

CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "CPU usage percent"
)

MEMORY_USAGE = Gauge(
    "system_memory_usage_percent",
    "Memory usage percent"
)

BACKEND_HEALTH = Gauge(
    "backend_server_health",
    "Backend health status",
    ["server"]
)

BACKEND_CONNECTIONS = Gauge(
    "backend_active_connections",
    "Backend active connections",
    ["server"]
)

# HOME

@app.get("/")
def home():
    return {
        "message": "Fault Tolerant Load Balancer Running",
        "strategy": strategy
    }

# =========================
# CHANGE STRATEGY
# =========================

@app.get("/strategy")
def change_strategy(type: str):

    global strategy

    if type in ["round_robin", "least_connections"]:
        strategy = type

    return {"strategy": strategy}

# BACKENDS

@app.get("/backends")
def backends():

    return {
        "backends": [
            {
                "url": server,
                "healthy": server_health[server],
                "connections": connections[server]
            }
            for server in servers
        ]
    }

# HEALTH CHECK LOOP
async def health_checker():

    while True:

        for server in servers:

            try:

                async with httpx.AsyncClient(timeout=2.0) as client:

                    response = await client.get(f"{server}/health")

                    if response.status_code == 200:
                        server_health[server] = True
                    else:
                        server_health[server] = False

            except:
                server_health[server] = False

            # Update Prometheus health metric
            BACKEND_HEALTH.labels(server=server).set(
                1 if server_health[server] else 0
            )

        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():

    asyncio.create_task(health_checker())

# SERVER SELECTION
def get_healthy_servers():

    return [
        server
        for server in servers
        if server_health[server]
    ]
def get_round_robin_server(healthy_servers):

    global current

    if not healthy_servers:
        return None

    server = healthy_servers[current % len(healthy_servers)]

    current += 1

    return server

def get_least_connection_server(healthy_servers):
    if not healthy_servers:
        return None

    return min(
        healthy_servers,
        key=lambda s: connections[s]
    )
# MAIN WORK ENDPOINT

@app.get("/work")
async def work(delay: int = Query(0)):

    REQUEST_COUNT.inc()
    ACTIVE_CONNECTIONS.inc()

    healthy_servers = get_healthy_servers()

    if not healthy_servers:

        ERROR_COUNT.inc()
        ACTIVE_CONNECTIONS.dec()

        raise HTTPException(
            status_code=503,
            detail="No healthy backend servers available"
        )

    # Select backend server
    if strategy == "round_robin":
        server = get_round_robin_server(healthy_servers)
    else:
        server = get_least_connection_server(healthy_servers)

    try:

        connections[server] += 1

        BACKEND_CONNECTIONS.labels(
            server=server
        ).set(connections[server])

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{server}/work",
                params={"delay": delay}
            )

        return response.json()

    except Exception as e:

        ERROR_COUNT.inc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        connections[server] -= 1

        BACKEND_CONNECTIONS.labels(
            server=server
        ).set(connections[server])

        ACTIVE_CONNECTIONS.dec()
# METRICS ENDPOINT
@app.get("/metrics")
def metrics():

    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )