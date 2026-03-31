from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ── USER ──────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

class UserOut(BaseModel):
    user_id: int
    name: str
    email: str
    phone: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── VEHICLE ───────────────────────────────────────────
class VehicleOut(BaseModel):
    vehicle_id: int
    type: str
    name: str
    number_code: str

    class Config:
        from_attributes = True


# ── ROUTE ─────────────────────────────────────────────
class RouteOut(BaseModel):
    route_id: int
    from_location: str
    to_location: str
    distance: Optional[int]

    class Config:
        from_attributes = True


# ── TRIP ──────────────────────────────────────────────
class TripSearchResult(BaseModel):
    trip_id: int
    vehicle_name: str
    vehicle_type: str
    number_code: str
    from_location: str
    to_location: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int

    class Config:
        from_attributes = True


class TripDetail(BaseModel):
    trip_id: int
    vehicle_id: int
    vehicle_name: str
    vehicle_type: str
    number_code: str
    route_id: int
    from_location: str
    to_location: str
    distance: Optional[int]
    departure_time: datetime
    arrival_time: datetime
    price: float

    class Config:
        from_attributes = True


# ── SEAT ──────────────────────────────────────────────
class SeatOut(BaseModel):
    seat_id: int
    seat_number: int
    status: str

    class Config:
        from_attributes = True


# ── UPDATE REQUESTS ───────────────────────────────────
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class TripUpdate(BaseModel):
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    price: Optional[float] = None


class BookRequest(BaseModel):
    # User info (create or find user)
    name: str
    email: str
    phone: str
    # Booking info
    trip_id: int
    seat_id: int
    booking_reference: str
    # Payment info
    amount: float
    payment_method: str   # card | upi | netbanking | wallet
    transaction_id: str

class BookingOut(BaseModel):
    booking_id: int
    booking_reference: str
    status: str
    booking_time: Optional[datetime]

    class Config:
        from_attributes = True


class BookingHistory(BaseModel):
    booking_id: int
    booking_reference: str
    booking_status: str
    booking_time: Optional[datetime]
    trip_id: int
    departure_time: datetime
    arrival_time: datetime
    price: float
    vehicle_name: str
    vehicle_type: str
    from_location: str
    to_location: str
    seat_number: int

    class Config:
        from_attributes = True