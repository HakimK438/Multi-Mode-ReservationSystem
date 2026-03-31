from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date, datetime, timedelta
import models, schemas


# ── TRIPS SEARCH ──────────────────────────────────────
def search_trips(db: Session, source: str, destination: str, travel_date: date, vehicle_type: str):
    start = datetime.combine(travel_date, datetime.min.time())
    end = start + timedelta(days=1)

    rows = (
        db.query(
            models.Trip.trip_id,
            models.Vehicle.name.label("vehicle_name"),
            models.Vehicle.type.label("vehicle_type"),
            models.Vehicle.number_code,
            models.Route.from_location,
            models.Route.to_location,
            models.Trip.departure_time,
            models.Trip.arrival_time,
            models.Trip.price,
            func.count(models.Seat.seat_id).label("available_seats"),
        )
        .join(models.Vehicle, models.Trip.vehicle_id == models.Vehicle.vehicle_id)
        .join(models.Route, models.Trip.route_id == models.Route.route_id)
        .outerjoin(
            models.Seat,
            and_(
                models.Seat.trip_id == models.Trip.trip_id,
                models.Seat.status == "available",
            ),
        )
        .filter(
            models.Route.from_location.ilike(f"%{source}%"),
            models.Route.to_location.ilike(f"%{destination}%"),
            models.Trip.departure_time >= start,
            models.Trip.departure_time < end,
            models.Vehicle.type == vehicle_type,
        )
        .group_by(
            models.Trip.trip_id,
            models.Vehicle.name,
            models.Vehicle.type,
            models.Vehicle.number_code,
            models.Route.from_location,
            models.Route.to_location,
            models.Trip.departure_time,
            models.Trip.arrival_time,
            models.Trip.price,
        )
        .order_by(models.Trip.departure_time)
        .all()
    )
    return rows


# ── TRIP DETAIL ───────────────────────────────────────
def get_trip_detail(db: Session, trip_id: int):
    row = (
        db.query(
            models.Trip.trip_id,
            models.Trip.vehicle_id,
            models.Vehicle.name.label("vehicle_name"),
            models.Vehicle.type.label("vehicle_type"),
            models.Vehicle.number_code,
            models.Trip.route_id,
            models.Route.from_location,
            models.Route.to_location,
            models.Route.distance,
            models.Trip.departure_time,
            models.Trip.arrival_time,
            models.Trip.price,
        )
        .join(models.Vehicle, models.Trip.vehicle_id == models.Vehicle.vehicle_id)
        .join(models.Route, models.Trip.route_id == models.Route.route_id)
        .filter(models.Trip.trip_id == trip_id)
        .first()
    )
    return row


# ── SEATS ─────────────────────────────────────────────
def get_available_seats(db: Session, trip_id: int):
    return (
        db.query(models.Seat)
        .filter(models.Seat.trip_id == trip_id, models.Seat.status == "available")
        .order_by(models.Seat.seat_number)
        .all()
    )


def get_all_seats(db: Session, trip_id: int):
    return (
        db.query(models.Seat)
        .filter(models.Seat.trip_id == trip_id)
        .order_by(models.Seat.seat_number)
        .all()
    )


def get_available_seat_count(db: Session, trip_id: int) -> int:
    return (
        db.query(func.count(models.Seat.seat_id))
        .filter(models.Seat.trip_id == trip_id, models.Seat.status == "available")
        .scalar()
    )


def check_seat_status(db: Session, seat_id: int):
    return db.query(models.Seat).filter(models.Seat.seat_id == seat_id).first()


# ── USER ──────────────────────────────────────────────
def get_user_by_email(db: Session, email: str):
    """Look up a user by their email address. Returns None if not found."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_or_create_user(db: Session, name: str, email: str, phone: str) -> models.User:
    """
    Find an existing user by email, or create a new one.
    This is called automatically during booking — so users are always
    registered in the DB when they make their first booking.

    NOTE: If a user with the same email already exists but provided
    a different phone/name, we do NOT overwrite their existing data
    (to avoid accidental data corruption). Only new users get created.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # New user — check phone uniqueness before inserting
        existing_phone = db.query(models.User).filter(models.User.phone == phone).first()
        if existing_phone:
            raise ValueError(
                f"Phone number {phone} is already registered with a different account. "
                "Please use your registered email or a different phone number."
            )
        user = models.User(name=name, email=email, phone=phone)
        db.add(user)
        db.flush()   # assigns user_id without committing the transaction
    return user


# ── BOOK (atomic: lock seat → create/find user → create booking → payment) ──
def book_ticket(db: Session, req: schemas.BookRequest):
    # 1. Lock the seat row to prevent double-booking (SELECT ... FOR UPDATE)
    seat = (
        db.query(models.Seat)
        .filter(models.Seat.seat_id == req.seat_id)
        .with_for_update()
        .first()
    )
    if not seat:
        raise ValueError("Seat not found")
    if seat.status != "available":
        raise ValueError("Seat is already booked. Please choose another seat.")

    # 2. Verify the seat belongs to the requested trip
    if seat.trip_id != req.trip_id:
        raise ValueError("Seat does not belong to the requested trip")

    # 3. Get or create the user (this is where user registration happens)
    user = get_or_create_user(db, req.name, req.email, req.phone)

    # 4. Mark seat as booked
    seat.status = "booked"

    # 5. Create the booking record
    booking = models.Booking(
        user_id=user.user_id,
        trip_id=req.trip_id,
        seat_id=seat.seat_id,
        booking_reference=req.booking_reference,
        status="confirmed",
    )
    db.add(booking)
    db.flush()  # assigns booking_id

    # 6. Record the payment
    payment = models.Payment(
        booking_id=booking.booking_id,
        amount=req.amount,
        payment_method=req.payment_method,
        status="success",
        transaction_id=req.transaction_id,
    )
    db.add(payment)

    # Transaction is committed by the caller (main.py) after this returns
    return booking


# ── BOOKING HISTORY ───────────────────────────────────
def get_user_bookings(db: Session, user_id: int):
    return (
        db.query(
            models.Booking.booking_id,
            models.Booking.booking_reference,
            models.Booking.status.label("booking_status"),
            models.Booking.booking_time,
            models.Trip.trip_id,
            models.Trip.departure_time,
            models.Trip.arrival_time,
            models.Trip.price,
            models.Vehicle.name.label("vehicle_name"),
            models.Vehicle.type.label("vehicle_type"),
            models.Route.from_location,
            models.Route.to_location,
            models.Seat.seat_number,
        )
        .join(models.Trip, models.Booking.trip_id == models.Trip.trip_id)
        .join(models.Vehicle, models.Trip.vehicle_id == models.Vehicle.vehicle_id)
        .join(models.Route, models.Trip.route_id == models.Route.route_id)
        .join(models.Seat, models.Booking.seat_id == models.Seat.seat_id)
        .filter(models.Booking.user_id == user_id)
        .order_by(models.Booking.booking_time.desc())
        .all()
    )


# ── UPDATE USER ───────────────────────────────────────
def update_user(db: Session, user_id: int, name: str = None, phone: str = None) -> models.User:
    """
    Update a user's name and/or phone number.
    Email is intentionally excluded — it's the user's identity key.
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise ValueError("User not found")
    if name is not None:
        user.name = name
    if phone is not None:
        # Check phone uniqueness against other accounts
        existing = db.query(models.User).filter(
            models.User.phone == phone,
            models.User.user_id != user_id
        ).first()
        if existing:
            raise ValueError(f"Phone number {phone} is already registered with another account.")
        user.phone = phone
    return user


def delete_user(db: Session, user_id: int) -> models.User:
    """
    Delete a user and all their associated data (cascades via FK).
    Only allowed if the user has no confirmed (active) bookings.
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise ValueError("User not found")
    active = db.query(models.Booking).filter(
        models.Booking.user_id == user_id,
        models.Booking.status == "confirmed"
    ).count()
    if active > 0:
        raise ValueError(
            f"Cannot delete account — {active} active booking(s) exist. "
            "Please cancel all bookings before deleting your account."
        )
    db.delete(user)
    return user


# ── UPDATE TRIP ────────────────────────────────────────
def update_trip(db: Session, trip_id: int, departure_time=None, arrival_time=None, price=None) -> models.Trip:
    """
    Update trip timing or price. Only non-None fields are changed.
    """
    trip = db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()
    if not trip:
        raise ValueError("Trip not found")
    if departure_time is not None:
        trip.departure_time = departure_time
    if arrival_time is not None:
        trip.arrival_time = arrival_time
    if price is not None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        trip.price = price
    return trip


def delete_trip(db: Session, trip_id: int) -> models.Trip:
    """
    Delete a trip. Blocked if any confirmed bookings exist for it.
    """
    trip = db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()
    if not trip:
        raise ValueError("Trip not found")
    active = db.query(models.Booking).filter(
        models.Booking.trip_id == trip_id,
        models.Booking.status == "confirmed"
    ).count()
    if active > 0:
        raise ValueError(
            f"Cannot delete trip — {active} confirmed booking(s) exist. "
            "Cancel all bookings for this trip first."
        )
    db.delete(trip)
    return trip


# ── CANCEL BOOKING ────────────────────────────────────
def cancel_booking(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise ValueError("Booking not found")
    if booking.status == "cancelled":
        raise ValueError("Booking is already cancelled")

    booking.status = "cancelled"

    # Free the seat so others can book it
    seat = db.query(models.Seat).filter(models.Seat.seat_id == booking.seat_id).first()
    if seat:
        seat.status = "available"

    return booking