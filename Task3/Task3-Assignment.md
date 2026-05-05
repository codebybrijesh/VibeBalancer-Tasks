# Task-3: Assignment

### Week 1 → Server Basics (FastAPI)

#### Objective

Understand how a server works and build a **backend service** that can handle requests. This server will later be used by a load balancer.

---

#### Assignment

Create a FastAPI server with basic endpoints that:

1. Respond to requests.
2. Simulate processing time.
3. Identify which server handled the request.

---

#### Requirements

1. **Server Identity**
   - Each server must have a name (e.g., `server_1`) and return this in every response.

2. **Endpoints**
   - **Home Endpoint** (`GET /`): Return a message like `{"message": "Hello from server_1"}`.
   - **Work Endpoint** (`GET /work`): Accept an optional `delay` query parameter, wait for the specified delay, and return the server name, delay, and status.
   - **Info Endpoint** (`GET /info`): Return the server name and current time.

3. **Run Multiple Servers**
   - Run at least two servers:
     - `server_1` → port 8001
     - `server_2` → port 8002

4. **Test**
   - Open `/work?delay=3` and observe the response after the delay.

---

#### Deliverables

- Two working backend servers.
- Delay simulation functionality.
- Each server identifiable by its name.

---

#### Key Insight

Right now, you have multiple servers but no system to manage them. This will lead into the concept of a load balancer in the next task.