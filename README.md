# Multi-Mode-ReservationSystem
A backend-driven reservation system supporting trains, flights, and ships with dynamic scheduling, seat allocation, and relational data modeling.
---

## Structure

```
routes → vehicles → trips → seats → bookings → payments
```

Each table has a clear responsibility and depends on the previous one.



## Core Logic

1. routes define all possible connections
2. vehicles represent transport (train, flight, ship)
3. trips connect vehicle + route + time
4. seats are generated per trip
5. bookings assign a seat to a user



## Constraint

```
UNIQUE (trip_id, seat_number)
```

Ensures a seat cannot be duplicated or booked twice.



## Behavior

1. routes are generated as combinations
2. trips are created using time (April 2026 schedule)
3. seats are dynamically created for every trip
4. same system works for all transport types



## Query

Trips are searched using:

```
from_location + to_location + date
```

---

## Tools

1. Python (FastAPI)
2. PostgreSQL (SQL, pgAdmin)
3. HTML, CSS, JavaScript
4. Git, GitHub



## Run

```
uvicorn main:app --reload
```

Open `frontend/index.html` for UI.




