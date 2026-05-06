# Client Script Observation

The client script sent 5 concurrent requests to the load balancer.

The load balancer distributed requests across both backend servers:

- http://localhost:8001
- http://localhost:8002

## Output

```text
Request 3 handled by: http://localhost:8001
Request 5 handled by: http://localhost:8001
Request 4 handled by: http://localhost:8002
Request 1 handled by: http://localhost:8002
Request 2 handled by: http://localhost:8002

Total Time Taken: 3.04 seconds
```

## Analysis

The order of completed requests was not sequential because requests were executed concurrently using threads.

The total execution time remained close to 3 seconds even though 5 requests were processed.

This demonstrates:

- concurrent request handling
- asynchronous processing
- effective load balancing

If requests were handled sequentially, the total time would have been approximately 15 seconds.