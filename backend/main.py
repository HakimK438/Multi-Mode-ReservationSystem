from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
import models, schemas, crud
from database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reservation API", version="2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── HEALTH CHECK ──────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Reservation API v2.1 is running"}


# ── TRIP SEARCH ───────────────────────────────────────
@app.get("/search-trips")
def search_trips(
    source: str = Query(...),
    destination: str = Query(...),
    travel_date: date = Query(...),
    vehicle_type: str = Query(...),   # train | flight | ship
    db: Session = Depends(get_db),
):
    rows = crud.search_trips(db, source, destination, travel_date, vehicle_type)
    result = []
    for r in rows:
        result.append({
            "trip_id": r.trip_id,
            "vehicle_name": r.vehicle_name,
            "vehicle_type": r.vehicle_type,
            "number_code": r.number_code,
            "from_location": r.from_location,
            "to_location": r.to_location,
            "departure_time": r.departure_time.isoformat(),
            "arrival_time": r.arrival_time.isoformat(),
            "price": float(r.price),
            "available_seats": r.available_seats,
        })
    return {"trips": result}


# ── TRIP DETAIL ───────────────────────────────────────
@app.get("/trip/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    row = crud.get_trip_detail(db, trip_id)
    if not row:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {
        "trip_id": row.trip_id,
        "vehicle_id": row.vehicle_id,
        "vehicle_name": row.vehicle_name,
        "vehicle_type": row.vehicle_type,
        "number_code": row.number_code,
        "route_id": row.route_id,
        "from_location": row.from_location,
        "to_location": row.to_location,
        "distance": row.distance,
        "departure_time": row.departure_time.isoformat(),
        "arrival_time": row.arrival_time.isoformat(),
        "price": float(row.price),
    }


# ── SEATS ─────────────────────────────────────────────
@app.get("/trip/{trip_id}/seats")
def get_all_seats(trip_id: int, db: Session = Depends(get_db)):
    seats = crud.get_all_seats(db, trip_id)
    return {
        "seats": [
            {"seat_id": s.seat_id, "seat_number": s.seat_number, "status": s.status}
            for s in seats
        ]
    }


@app.get("/trip/{trip_id}/available-seats")
def get_available_seats(trip_id: int, db: Session = Depends(get_db)):
    seats = crud.get_available_seats(db, trip_id)
    return {"available_seats": [{"seat_id": s.seat_id, "seat_number": s.seat_number} for s in seats]}


@app.get("/trip/{trip_id}/available-seat-count")
def get_seat_count(trip_id: int, db: Session = Depends(get_db)):
    count = crud.get_available_seat_count(db, trip_id)
    return {"trip_id": trip_id, "available_seats": count}


@app.get("/seat/{seat_id}/status")
def seat_status(seat_id: int, db: Session = Depends(get_db)):
    seat = crud.check_seat_status(db, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    return {"seat_id": seat.seat_id, "trip_id": seat.trip_id, "seat_number": seat.seat_number, "status": seat.status}


# ── BOOK TICKET (atomic: creates user if new, marks seat booked, saves payment) ──
@app.post("/book")
def book_ticket(req: schemas.BookRequest, db: Session = Depends(get_db)):
    try:
        booking = crud.book_ticket(db, req)
        db.commit()
        db.refresh(booking)
        return {
            "message": "Booking successful",
            "booking_id": booking.booking_id,
            "booking_reference": booking.booking_reference,
            "status": booking.status,
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── USER LOOKUP BY EMAIL (NEW — used by "My Bookings" page) ──────────────────
@app.get("/user/by-email")
def get_user_by_email(email: str = Query(...), db: Session = Depends(get_db)):
    """
    Look up a user by email address.
    Returns user_id, name, email, phone.
    Used by the frontend to find a user before loading their booking history.
    """
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
    }


# ── USER BOOKING HISTORY ──────────────────────────────
@app.get("/user/{user_id}/bookings")
def user_bookings(user_id: int, db: Session = Depends(get_db)):
    rows = crud.get_user_bookings(db, user_id)
    result = []
    for r in rows:
        result.append({
            "booking_id": r.booking_id,
            "booking_reference": r.booking_reference,
            "booking_status": r.booking_status,
            "booking_time": r.booking_time.isoformat() if r.booking_time else None,
            "trip_id": r.trip_id,
            "departure_time": r.departure_time.isoformat(),
            "arrival_time": r.arrival_time.isoformat(),
            "price": float(r.price),
            "vehicle_name": r.vehicle_name,
            "vehicle_type": r.vehicle_type,
            "from_location": r.from_location,
            "to_location": r.to_location,
            "seat_number": r.seat_number,
        })
    return {"bookings": result}


# ── UPDATE USER ───────────────────────────────────────
@app.patch("/user/{user_id}")
def update_user(user_id: int, req: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Partially update a user's name and/or phone number.
    Email cannot be changed (it's the identity key).
    """
    try:
        user = crud.update_user(db, user_id, name=req.name, phone=req.phone)
        db.commit()
        db.refresh(user)
        return {
            "message": "User updated successfully",
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── DELETE USER ───────────────────────────────────────
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user account. Blocked if any confirmed bookings exist.
    All historical (cancelled) bookings are removed via cascade.
    """
    try:
        user = crud.delete_user(db, user_id)
        db.commit()
        return {"message": f"User '{user.name}' (id={user_id}) deleted successfully"}
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── UPDATE TRIP ────────────────────────────────────────
@app.patch("/trip/{trip_id}")
def update_trip(trip_id: int, req: schemas.TripUpdate, db: Session = Depends(get_db)):
    """
    Partially update a trip's departure time, arrival time, and/or price.
    """
    try:
        trip = crud.update_trip(
            db, trip_id,
            departure_time=req.departure_time,
            arrival_time=req.arrival_time,
            price=req.price,
        )
        db.commit()
        db.refresh(trip)
        return {
            "message": "Trip updated successfully",
            "trip_id": trip.trip_id,
            "departure_time": trip.departure_time.isoformat(),
            "arrival_time": trip.arrival_time.isoformat(),
            "price": float(trip.price),
        }
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── DELETE TRIP ────────────────────────────────────────
@app.delete("/trip/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """
    Delete a trip. Blocked if any confirmed bookings exist for it.
    """
    try:
        trip = crud.delete_trip(db, trip_id)
        db.commit()
        return {"message": f"Trip {trip_id} deleted successfully"}
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/booking/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = crud.cancel_booking(db, booking_id)
        db.commit()
        return {"message": "Booking cancelled successfully", "booking_id": booking.booking_id}
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))