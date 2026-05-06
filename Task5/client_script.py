import requests
import threading
import time

URL = "http://localhost:8000/work?delay=3"


def send_request(number):

    response = requests.get(URL)

    data = response.json()

    print(f"Request {number} handled by: {data['handled_by']}")


threads = []

start = time.time()

for i in range(5):

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