# importing things we need to build the server
from fastapi import FastAPI, Query
import time  # used to create delay (like fake processing)
from datetime import datetime  # to get current time
import os  # to read environment variables (like server name)

# creating our FastAPI app (basically starting the server)
app = FastAPI()

# getting server name from system
# if nothing is set, it will just use "default_server"
SERVER_NAME = os.getenv("SERVER_NAME", "default_server")

# this runs when someone opens "/"
@app.get("/")
def home():
    # just returning a simple message with server name
    return {"message": f"Hello from {SERVER_NAME}"}

# this runs when someone opens "/work"
import asyncio
@app.get("/work")
async def do_work(delay: int = Query(0, description="Delay in seconds")):
    # delay means how many seconds we want to wait
    # if user doesn't give anything, it will be 0 by default

    # this line makes the server wait (like doing some heavy work)
    await asyncio.sleep(delay)

    # after waiting, we send back the response
    return {
        "server": SERVER_NAME,   # which server handled it
        "delay": delay,          # how long we waited
        "status": "completed"   # just a simple message
    }

# this runs when someone opens "/info"
@app.get("/info")
def info():
    return {
        "server": SERVER_NAME,

        # getting current time and formatting it nicely
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }