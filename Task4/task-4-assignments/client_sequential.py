import requests
import time

URL = "http://localhost:8001/work?delay=3"

start = time.time()

for i in range(5):
    print(f"Sending request {i+1}")

    response = requests.get(URL)

    print(f"Response {i+1}: {response.json()}")

end = time.time()

print(f"\nTotal Time Taken: {end - start:.2f} seconds")