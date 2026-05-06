
from fastapi import FastAPI, Query
import time 
from datetime import datetime
import os  # to read environment variables (like server name)

app = FastAPI()


SERVER_NAME = os.getenv("SERVER_NAME", "default_server")



@app.get("/")
def home():
    # just returning a simple message with server name
    return {"message": f"Hello from {SERVER_NAME}"}



from datetime import datetime

@app.get("/work")
def do_work(delay: int = Query(0)):
    start_time = datetime.now()
    print(f"START at {start_time}")

    time.sleep(delay)

    end_time = datetime.now()
    print(f"END at {end_time}")

    return {"status": "done"}


# this runs when someone opens "/info"
@app.get("/info")
def info():
    return {
        "server": SERVER_NAME,

        # getting current time and formatting it nicely
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
