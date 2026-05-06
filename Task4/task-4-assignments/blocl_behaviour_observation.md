
START at 2026-05-06 08:40:23.160461
END at 2026-05-06 08:40:26.160655
INFO:     127.0.0.1:51640 - "GET /work?delay=3 HTTP/1.1" 200 OK
START at 2026-05-06 08:40:26.166177
END at 2026-05-06 08:40:29.166337
INFO:     127.0.0.1:51640 - "GET /work?delay=3 HTTP/1.1" 200 OK
START at 2026-05-06 08:40:29.171499
END at 2026-05-06 08:40:32.171649
INFO:     127.0.0.1:51640 - "GET /work?delay=3 HTTP/1.1" 200 OK

Each request waits for the previous one to finish.
Requests are processed one after another.
Your server is currently behaving as a blocking/synchronous server.
This is because of this part of the code:
time.sleep(delay)
time.sleep() blocks the current thread completely