import requests
import threading
import time

URL = "http://localhost:8000/work?delay=3"


def send_request(number):

    try:

        response = requests.get(URL)

        data = response.json()

        print(f"Request {number} handled by: {data['handled_by']}")

    except Exception as e:

        print(f"Request {number} failed: {e}")


threads = []

start = time.time()

for i in range(10):

    t = threading.Thread(
        target=send_request,
        args=(i + 1,)
    )

    threads.append(t)

    t.start()

for t in threads:
    t.join()

end = time.time()

print(f"\nTotal Time Taken: {end - start:.2f} seconds")