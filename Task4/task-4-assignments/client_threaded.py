import requests
import threading
import time

URL = "http://localhost:8001/work?delay=3"

def send_request(number):
    print(f"Starting Request {number}")

    response = requests.get(URL)

    print(f"Finished Request {number}: {response.json()}")


threads = []

start = time.time()


for i in range(5):
    t = threading.Thread(target=send_request, args=(i+1,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()

print(f"\nTotal Time Taken: {end - start:.2f} seconds")

