# Fault Tolerance Observation

## Before Fault Tolerance

Initially, the load balancer forwarded requests to backend servers without checking whether they were alive.

When one backend server stopped:

- the load balancer still attempted to forward requests to it
- connection errors occurred
- some client requests failed

The system was not reliable because failed servers were still receiving traffic.

---

# After Adding Health Checks

Health check endpoints were added to all backend servers.

The load balancer periodically checked:

GET /health

for each backend server.

Healthy servers were marked as:

```python
True
```

Unhealthy servers were marked as:

```python
False
```

---

# Unhealthy Server Skipping

When a backend server failed:

- the load balancer automatically marked it unhealthy
- traffic was redirected only to healthy servers
- users continued receiving successful responses

Example:

- server_1 down
- all traffic forwarded to server_2

---

# Retry Logic

If a selected backend failed during request forwarding:

- the load balancer retried the request using another healthy backend
- failed backends were marked unhealthy immediately

This improved reliability and reduced request failures.

---

# Recovery Detection

When a stopped backend server restarted:

- the periodic health checker detected recovery
- the server became healthy again
- traffic distribution resumed normally

---

# All Servers Down

When all backend servers were stopped:

- the load balancer returned:

503 Service Unavailable

instead of crashing.

This provided proper fault handling for clients.

---

# Conclusion

Fault tolerance significantly improved system reliability.

The load balancer could now:

- detect failed backend servers
- avoid unhealthy servers
- retry failed requests
- recover automatically when servers restarted

This behavior resembles real-world distributed systems and production load balancers.