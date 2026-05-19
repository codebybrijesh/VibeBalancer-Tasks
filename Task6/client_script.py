import time
import requests
import concurrent.futures

LB_URL = "http://127.0.0.1:8000"


def send_request(url, number):
    try:
        response = requests.get(url)
        data = response.json()
        print(
            f"Request {number} handled by: "
            f"{data['server']}"
        )
    except Exception as e:
        print(f"Request {number} failed: {e}")
print("\n===== ROUND ROBIN TEST =====")
requests.get(
    f"{LB_URL}/strategy",
    params={"type": "round_robin"}
)
urls = []
for i in range(10):

    urls.append(
        f"{LB_URL}/work?delay=3"
    )
start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:

    for i, url in enumerate(urls):

        executor.submit(
            send_request,
            url,
            i + 1
        )
finish = time.perf_counter()
print(
    f"\nFinished in "
    f"{round(finish - start, 2)} second(s)"
)
print("\n===== LEAST CONNECTIONS TEST =====")
requests.get(
    f"{LB_URL}/strategy",
    params={"type": "least_connections"}
)
urls = []
for i in range(10):

    urls.append(
        f"{LB_URL}/work?delay={i % 5}"
    )
start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:

    for i, url in enumerate(urls):

        executor.submit(
            send_request,
            url,
            i + 1
        )

finish = time.perf_counter()
print(
    f"\nFinished in "
    f"{round(finish - start, 2)} second(s)"
)
print("\n===== METRICS =====")
metrics = requests.get(
    f"{LB_URL}/metrics"
)

import json

print(
    json.dumps(
        metrics.json(),
        indent=4
    )
)

print("""

Observations:

1. Round Robin Algorithm
- Requests are distributed one after another.
- All servers receive nearly equal requests.
- Current server load is not considered.

2. Least Connections Algorithm
- Requests are distributed dynamically.
- Server with fewer active connections receives the next request.
- Better for varying request delays.

3. Metrics Endpoint
- Tracks total requests.
- Shows active connections.
- Displays CPU and memory usage.

""")