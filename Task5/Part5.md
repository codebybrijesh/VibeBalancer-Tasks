# Part 5: Compare Algorithms

# Round Robin Algorithm

## Is the distribution equal?

Yes.  
The Round Robin algorithm distributes requests equally among all backend servers.

Example:

- Request 1 → server_1
- Request 2 → server_2
- Request 3 → server_1
- Request 4 → server_2

This ensures fair and simple traffic distribution.

---

## Does it consider server load?

No.  
Round Robin does not check whether a server is busy or free.

It forwards requests in a fixed cyclic order even if one server is handling many long-running requests.

Because of this, some servers may become overloaded while others remain less utilized.

---

# Least Connections Algorithm

## Does it adapt to varying delays?

Yes.  
Least Connections dynamically checks the number of active connections on each server before forwarding a request.

If one server is busy handling long-delay requests, new requests are sent to the server with fewer active connections.

This makes the algorithm more adaptive and efficient under uneven workloads.

---

## Are faster servers used more frequently?

Yes.  
Faster servers complete requests sooner, reducing their active connection count more quickly.

As a result, the load balancer selects them more often because they appear less busy.

This improves overall resource utilization and response performance.

---

# Conclusion

- Round Robin is simple and provides equal distribution.
- Least Connections is smarter because it adapts to server load dynamically.
- Least Connections performs better when request durations vary significantly.