# Async Server Observation

The server logs show that all requests started almost at the same time and also completed nearly together after approximately **3 seconds**.

This demonstrates **non-blocking asynchronous behavior**.

Unlike the blocking implementation, the server did not wait for one request to finish before starting the next request.

The async implementation used:

```python
await asyncio.sleep(delay)
```

instead of:

```python
time.sleep(delay)
```

which allowed the FastAPI event loop to handle multiple requests concurrently.

## Server Logs

```text
START at 2026-05-06 10:39:24.824519
START at 2026-05-06 10:39:24.825022
START at 2026-05-06 10:39:24.827567
START at 2026-05-06 10:39:24.828489
START at 2026-05-06 10:39:24.828718

END at 2026-05-06 10:39:27.825320
INFO:     127.0.0.1:55388 - "GET /work?delay=3 HTTP/1.1" 200 OK

END at 2026-05-06 10:39:27.826414
INFO:     127.0.0.1:55386 - "GET /work?delay=3 HTTP/1.1" 200 OK

END at 2026-05-06 10:39:27.827991
INFO:     127.0.0.1:55390 - "GET /work?delay=3 HTTP/1.1" 200 OK

END at 2026-05-06 10:39:27.828731
INFO:     127.0.0.1:55392 - "GET /work?delay=3 HTTP/1.1" 200 OK

END at 2026-05-06 10:39:27.829138
INFO:     127.0.0.1:55406 - "GET /work?delay=3 HTTP/1.1" 200 OK
```

## Conclusion

Using asynchronous programming with FastAPI enables efficient concurrent request handling and significantly improves scalability and responsiveness.