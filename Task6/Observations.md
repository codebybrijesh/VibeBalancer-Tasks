# Metrics Observation

The `/metrics` endpoint successfully exposed both application-level and system-level metrics.

## Metrics Response

```json
{"application":{"total_requests":20.0,"active_connections":0.0,"total_errors":0.0},"system":{"cpu_usage_percent":2.7,"memory_usage_percent":23.4},"backend_servers":{"server_1":{"healthy":true,"active_connections":0},"server_2":{"healthy":true,"active_connections":0}},"current_strategy":"least_connections"}
```

---

# Analysis

## Application Metrics

- `total_requests` increased to 20 after running the concurrent client script.
- `active_connections` returned to 0 after all requests completed.
- `total_errors` remained 0, indicating successful request handling.

## System Metrics

- CPU usage increased slightly during concurrent traffic.
- Memory usage remained stable.

The low CPU utilization was expected because the workload primarily used asynchronous waiting (`asyncio.sleep`) rather than CPU-intensive computation.

---

# Conclusion

The metrics endpoint enabled real-time visibility into:

- request traffic
- active system load
- backend reliability
- hardware utilization

This forms the foundation for advanced monitoring and auto-scaling systems used in distributed infrastructure.