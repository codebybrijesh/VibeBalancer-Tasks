# Observation

The sequential client sent **5 requests** to the FastAPI server.

Each request took approximately **3 seconds** to complete.

The total execution time was around **15 seconds**, proving that requests were handled **one after another**.

This demonstrates **blocking behavior** because the server uses:

```python
time.sleep()
```

which blocks the execution thread until the task is completed.

## Output

```text
Sending request 1
Response 1: {'status': 'done'}

Sending request 2
Response 2: {'status': 'done'}

Sending request 3
Response 3: {'status': 'done'}

Sending request 4
Response 4: {'status': 'done'}

Sending request 5
Response 5: {'status': 'done'}

Total Time Taken: 15.04 seconds
```