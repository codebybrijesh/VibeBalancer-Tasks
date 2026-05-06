from fastapi import FastAPI, Query
import httpx

# Creating the FastAPI app
# This app will behave like a Load Balancer
app = FastAPI()


# List of backend servers
# These are the actual servers that will handle the work
servers = [
    "http://localhost:8001",
    "http://localhost:8002"
]


# ROUND ROBIN VARIABLES

# I made this variable to keep track of
# which server should receive the next request.
# Example:
# Request 1 -> server_1
# Request 2 -> server_2
# Request 3 -> server_1 again
current = 0


#LEAST CONNECTION VARIABLES

# Here I am storing how many active requests
# each server is currently handling.
#
# This helps in Least Connections Algorithm.
#
# Example:
# server_1 -> 2 active users
# server_2 -> 1 active user
#
# Then the next request will go to server_2
# because it is less busy.
connections = {
    "http://localhost:8001": 0,
    "http://localhost:8002": 0
}


# STRATEGY SELECTION

# Default strategy is Round Robin
# User can later change it using /strategy endpoint
strategy = "round_robin"


# HOME ROUTE

@app.get("/")
def home():

    # Simple route to check if Load Balancer is running
    return {
        "message": "Load Balancer Running",
        "strategy": strategy
    }


# CHANGE STRATEGY ROUTE

@app.get("/strategy")
def change_strategy(type: str):

    # Using global because I want to modify
    # the strategy variable declared outside.
    global strategy

    # Allowing only valid strategies
    if type in ["round_robin", "least_connections"]:
        strategy = type

    return {
        "strategy": strategy
    }


# ROUND ROBIN FUNCTION

def get_round_robin_server():

    global current

    # Selecting current server
    server = servers[current]

    # Moving index to next server
    # % len(servers) makes it circular
    #
    # Example:
    # current = 0 -> server_1
    # current = 1 -> server_2
    # current = 2 -> back to server_1
    current = (current + 1) % len(servers)

    return server

# LEAST CONNECTION FUNCTION
def get_least_connection_server():

    # Selecting the server with minimum active connections
    #
    # connections.get tells Python to compare values
    #
    # Example:
    # {
    #   server_1: 5,
    #   server_2: 2
    # }
    #
    # Then server_2 will be selected
    return min(connections, key=connections.get)


#MAIN WORK ROUTE

@app.get("/work")
async def work(delay: int = Query(0)):

    # Checking which algorithm is currently active

    if strategy == "round_robin":

        # Using Round Robin Algorithm
        server = get_round_robin_server()

    else:

        # Using Least Connections Algorithm
        server = get_least_connection_server()


    # Increasing active connection count
    # because this server is now handling a request
    connections[server] += 1


    # Printing logs for understanding flow
    print(f"\nForwarding request to {server}")
    print(f"Current Connections: {connections}")


    try:

        # AsyncClient helps in making async HTTP requests
        # This makes the load balancer non-blocking
        async with httpx.AsyncClient() as client:

            # Forwarding request to backend server
            response = await client.get(

                # Calling backend /work endpoint
                f"{server}/work",

                # Passing delay parameter to backend
                params={"delay": delay}
            )

            # Converting backend response into JSON
            data = response.json()


            # Returning final response to user
            return {

                # Which backend handled the request
                "handled_by": server,

                # Actual backend response
                "backend_response": data
            }


    finally:

        # Reducing connection count after request finishes
        #
        # finally block ensures this always runs
        # even if an error occurs.
        connections[server] -= 1

        print(f"Request completed on {server}")
        print(f"Updated Connections: {connections}")