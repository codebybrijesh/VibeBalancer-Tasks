from fastapi import FastAPI, Query, HTTPException
import httpx
import asyncio
import psutil

app = FastAPI()

servers = [
    "http://localhost:8001",
    "http://localhost:8002"
]

# round robin pointer
current = 0

# active connections
connections = {
    "http://localhost:8001": 0,
    "http://localhost:8002": 0
}

# backend health
server_health = {
    "http://localhost:8001": True,
    "http://localhost:8002": True
}

# strategy
strategy = "round_robin"


@app.get("/")
def home():
    return {
        "message": "Fault Tolerant Load Balancer Running",
        "strategy": strategy
    }


@app.get("/strategy")
def change_strategy(type: str):

    global strategy

    if type in ["round_robin", "least_connections"]:
        strategy = type

    return {"strategy": strategy}


@app.get("/backends")
def backends():

    return {
        "backends": [
            {
                "url": server,
                "healthy": server_health[server]
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

        print("\nServer Health:")
        print(server_health)

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

    global total_requests
    global active_connections
    global total_errors

    total_requests += 1
    active_connections += 1

    healthy_servers = get_healthy_servers()

    if not healthy_servers:

        total_errors += 1

        active_connections -= 1

        raise HTTPException(
            status_code=503,
            detail="No healthy backend servers available"
        )

    try:

        # existing forwarding logic here

        pass

    except Exception:

        total_errors += 1

        raise

    finally:

        active_connections -= 1

# APPLICATION METRICS

total_requests = 0
active_connections = 0
total_errors = 0

@app.get("/metrics")
def metrics():

    return {

        "application": {

            "total_requests": total_requests,

            "active_connections": active_connections,

            "total_errors": total_errors
        },

        "system": {

            "cpu_usage_percent": psutil.cpu_percent(),

            "memory_usage_percent": psutil.virtual_memory().percent
        }
    }