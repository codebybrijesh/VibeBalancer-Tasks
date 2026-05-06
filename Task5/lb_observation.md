# Load Balancer Observation

The custom FastAPI load balancer successfully distributed requests across two backend servers.

## Round Robin Behavior

Requests alternated between:

- server_1 → http://localhost:8001
- server_2 → http://localhost:8002

Example distribution:

- Request 1 → server_1
- Request 2 → server_2
- Request 3 → server_1
- Request 4 → server_2

This confirms that the Round Robin algorithm distributed traffic equally.

---

## Connection Tracking

The load balancer tracked active connections for each server.

Example:

```text
Current Connections:
{
  'http://localhost:8001': 1,
  'http://localhost:8002': 1
}
```

This showed that multiple requests were handled concurrently.

---

## Least Connections Insight

The Least Connections algorithm dynamically selects the server with the fewest active requests.

This allows better utilization when some servers are busy handling long-running requests.

---

## Conclusion

Round Robin ensures equal distribution of requests.

Least Connections adapts better to varying server loads and improves efficiency in concurrent systems.

This assignment demonstrated the core concepts behind real-world distributed systems and load balancers.