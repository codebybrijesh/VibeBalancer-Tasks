from fastapi import FastAPI, Query
from datetime import datetime
import asyncio
import os

app = FastAPI()

SERVER_NAME = os.getenv("SERVER_NAME", "default_server")


@app.get("/")
def home():
    return {"message": f"Hello from {SERVER_NAME}"}


@app.get("/work")
async def do_work(delay: int = Query(0)):

    start_time = datetime.now()

    print(f"START at {start_time}")

    await asyncio.sleep(delay)

    end_time = datetime.now()

    print(f"END at {end_time}")

    return {"status": "done"}


@app.get("/info")
def info():
    return {
        "server": SERVER_NAME,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }