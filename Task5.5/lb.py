from fastapi import FastAPI, Query, HTTPException
import httpx
import asyncio

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

    healthy_servers = get_healthy_servers()

    if not healthy_servers:

        raise HTTPException(
            status_code=503,
            detail="No healthy backend servers available"
        )

    # select server
    if strategy == "round_robin":
        server = get_round_robin_server(healthy_servers)
    else:
        server = get_least_connection_server(healthy_servers)

    # try request
    try:

        connections[server] += 1

        print(f"\nForwarding request to {server}")
        print(f"Connections: {connections}")

        async with httpx.AsyncClient(timeout=10.0) as client:

            response = await client.get(
                f"{server}/work",
                params={"delay": delay}
            )

            return {
                "handled_by": server,
                "backend_response": response.json()
            }

    except Exception as e:

        print(f"\nServer failed: {server}")

        server_health[server] = False

        # retry using another server
        retry_servers = [
            s for s in healthy_servers
            if s != server
        ]

        if not retry_servers:

            raise HTTPException(
                status_code=503,
                detail="All backend servers unavailable"
            )

        retry_server = retry_servers[0]

        try:

            async with httpx.AsyncClient(timeout=10.0) as client:

                response = await client.get(
                    f"{retry_server}/work",
                    params={"delay": delay}
                )

                return {
                    "handled_by": retry_server,
                    "backend_response": response.json(),
                    "retry": True
                }

        except:

            raise HTTPException(
                status_code=503,
                detail="All backend servers unavailable"
            )

    finally:

        if server in connections:
            connections[server] -= 1