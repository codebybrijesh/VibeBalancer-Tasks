from fastapi import FastAPI, Query
import asyncio
from datetime import datetime

app = FastAPI()

SERVER_NAME = "server_1"


@app.get("/")
def home():
    return {"message": f"Hello from {SERVER_NAME}"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "server": SERVER_NAME
    }


@app.get("/work")
async def work(delay: int = Query(0)):

    start = datetime.now()

    print(f"{SERVER_NAME} START at {start}")

    await asyncio.sleep(delay)

    end = datetime.now()

    print(f"{SERVER_NAME} END at {end}")

    return {
        "server": SERVER_NAME,
        "status": "done"
    }