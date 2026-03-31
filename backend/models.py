from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey,
    CheckConstraint, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    bookings = relationship("Booking", back_populates="user")


class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = (
        CheckConstraint("type IN ('train', 'flight', 'ship')", name="ck_vehicle_type"),
    )

    vehicle_id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    number_code = Column(String(20), unique=True, nullable=False)

    trips = relationship("Trip", back_populates="vehicle")


class Route(Base):
    __tablename__ = "routes"
    __table_args__ = (
        CheckConstraint("distance > 0", name="ck_route_distance"),
    )

    route_id = Column(Integer, primary_key=True, index=True)
    from_location = Column(String(100), nullable=False)
    to_location = Column(String(100), nullable=False)
    distance = Column(Integer)

    trips = relationship("Trip", back_populates="route")


class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_trip_price"),
    )

    trip_id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    vehicle = relationship("Vehicle", back_populates="trips")
    route = relationship("Route", back_populates="trips")
    seats = relationship("Seat", back_populates="trip")
    bookings = relationship("Booking", back_populates="trip")


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        CheckConstraint("status IN ('available', 'booked')", name="ck_seat_status"),
        UniqueConstraint("trip_id", "seat_number", name="uq_trip_seat"),
    )

    seat_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    status = Column(String(20), default="available")

    trip = relationship("Trip", back_populates="seats")
    booking = relationship("Booking", back_populates="seat", uselist=False)


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("status IN ('confirmed', 'cancelled')", name="ck_booking_status"),
    )

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.seat_id", ondelete="CASCADE"), unique=True, nullable=False)
    booking_reference = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), default="confirmed")
    booking_time = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")
    seat = relationship("Seat", back_populates="booking")
    payment = relationship("Payment", back_populates="booking", uselist=False)


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_payment_amount"),
        CheckConstraint(
            "payment_method IN ('card', 'upi', 'netbanking', 'wallet')",
            name="ck_payment_method"
        ),
        CheckConstraint(
            "status IN ('success', 'failed', 'pending')",
            name="ck_payment_status"
        ),
    )

    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(20), nullable=False)
    status = Column(String(20), default="success")
    transaction_id = Column(String(100), unique=True)

    booking = relationship("Booking", back_populates="payment")