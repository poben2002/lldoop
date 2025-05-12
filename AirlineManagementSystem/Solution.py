from enum import Enum
import uuid
from datetime import datetime


class Role(Enum):
    PASSENGER = "Passenger"
    STAFF = "Staff"
    ADMIN = "Admin"


class SeatClass(Enum):
    ECONOMY = "Economy"
    BUSINESS = "Business"
    FIRST = "First"


class User:
    def __init__(self, name, email, role=Role.PASSENGER):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role


class Aircraft:
    def __init__(self, model, capacity):
        self.id = str(uuid.uuid4())
        self.model = model
        self.capacity = capacity
        self.seat_map = {i: None for i in range(1, capacity + 1)}  # seat_number: user_id

    def assign_seat(self, seat_number, user_id):
        if self.seat_map.get(seat_number) is None:
            self.seat_map[seat_number] = user_id
            return True
        return False

    def get_available_seats(self):
        return [s for s, u in self.seat_map.items() if u is None]


class Flight:
    def __init__(self, source, destination, date, aircraft):
        self.id = str(uuid.uuid4())
        self.source = source
        self.destination = destination
        self.date = date
        self.aircraft = aircraft
        self.crew = []
        self.bookings = []

    def add_crew(self, staff_user):
        self.crew.append(staff_user)

    def get_available_seats(self):
        return self.aircraft.get_available_seats()


class Baggage:
    def __init__(self, weight_kg, is_carry_on):
        self.id = str(uuid.uuid4())
        self.weight_kg = weight_kg
        self.is_carry_on = is_carry_on


class BookingStatus(Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"


class Booking:
    def __init__(self, passenger, flight, seat_number, baggage_list):
        self.id = str(uuid.uuid4())
        self.passenger = passenger
        self.flight = flight
        self.seat_number = seat_number
        self.baggage = baggage_list
        self.status = BookingStatus.CONFIRMED
        self.timestamp = datetime.now()

    def cancel(self):
        self.status = BookingStatus.CANCELLED

    def refund(self):
        self.status = BookingStatus.REFUNDED


class Payment:
    def __init__(self, booking_id, amount, method):
        self.id = str(uuid.uuid4())
        self.booking_id = booking_id
        self.amount = amount
        self.method = method
        self.timestamp = datetime.now()


class AirlineSystem:
    def __init__(self):
        self.users = {}
        self.flights = []
        self.bookings = {}
        self.payments = []

    def register_user(self, name, email, role=Role.PASSENGER):
        user = User(name, email, role)
        self.users[user.id] = user
        return user

    def add_flight(self, source, destination, date, aircraft):
        flight = Flight(source, destination, date, aircraft)
        self.flights.append(flight)
        return flight

    def search_flights(self, source, destination, date):
        return [f for f in self.flights if f.source == source and f.destination == destination and f.date == date]

    def book_flight(self, passenger_id, flight_id, seat_number, baggage_weights):
        passenger = self.users[passenger_id]
        flight = next((f for f in self.flights if f.id == flight_id), None)
        if not flight or not flight.aircraft.assign_seat(seat_number, passenger_id):
            return None
        baggage_list = [Baggage(w, False) for w in baggage_weights]
        booking = Booking(passenger, flight, seat_number, baggage_list)
        flight.bookings.append(booking)
        self.bookings[booking.id] = booking
        return booking

    def process_payment(self, booking_id, amount, method):
        payment = Payment(booking_id, amount, method)
        self.payments.append(payment)
        return payment

    def cancel_booking(self, booking_id):
        booking = self.bookings.get(booking_id)
        if booking:
            booking.cancel()
            return True
        return False

    def issue_refund(self, booking_id):
        booking = self.bookings.get(booking_id)
        if booking and booking.status == BookingStatus.CANCELLED:
            booking.refund()
            return True
        return False
