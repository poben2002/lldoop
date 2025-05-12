import uuid
from datetime import datetime
from threading import Lock
from collections import defaultdict


class Seat:
    def __init__(self, row, number):
        self.id = str(uuid.uuid4())
        self.row = row
        self.number = number
        self.is_booked = False
        self.lock = Lock()  # For concurrency protection


class Concert:
    def __init__(self, artist, venue, date, time, seat_rows, seats_per_row):
        self.id = str(uuid.uuid4())
        self.artist = artist
        self.venue = venue
        self.date = date
        self.time = time
        self.seats = self._generate_seats(seat_rows, seats_per_row)
        self.waitlist = []

    def _generate_seats(self, rows, seats_per_row):
        return {(r, n): Seat(r, n) for r in range(1, rows + 1) for n in range(1, seats_per_row + 1)}

    def get_available_seats(self):
        return [seat for seat in self.seats.values() if not seat.is_booked]

    def search_seats(self, row=None):
        return [
            seat for (r, _), seat in self.seats.items()
            if not seat.is_booked and (row is None or r == row)
        ]


class Booking:
    def __init__(self, user_id, concert_id, seat_ids, total_price):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.concert_id = concert_id
        self.seat_ids = seat_ids
        self.status = "CONFIRMED"
        self.timestamp = datetime.now()
        self.total_price = total_price


class User:
    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.bookings = []


class PaymentProcessor:
    @staticmethod
    def process_payment(user_id, amount, method):
        print(f"[Payment] Processing {amount} via {method} for user {user_id}")
        return True  # Simulate success


class NotificationService:
    @staticmethod
    def send_confirmation(email, booking_id):
        print(f"[Notification] Sent confirmation to {email} for booking {booking_id}")


class TicketSystem:
    def __init__(self):
        self.users = {}
        self.concerts = []
        self.bookings = []

    def register_user(self, name, email):
        user = User(name, email)
        self.users[user.id] = user
        return user

    def add_concert(self, artist, venue, date, time, rows, seats_per_row):
        concert = Concert(artist, venue, date, time, rows, seats_per_row)
        self.concerts.append(concert)
        return concert

    def search_concerts(self, artist=None, venue=None, date=None):
        results = []
        for concert in self.concerts:
            if (not artist or concert.artist == artist) and \
               (not venue or concert.venue == venue) and \
               (not date or concert.date == date):
                results.append(concert)
        return results

    def book_seats(self, user_id, concert_id, seat_coords, payment_method):
        user = self.users[user_id]
        concert = next(c for c in self.concerts if c.id == concert_id)
        seat_objs = []

        # Lock and validate seats
        try:
            for coord in seat_coords:
                seat = concert.seats[coord]
                if not seat.lock.acquire(timeout=3):  # Try to acquire lock
                    raise Exception("Seat is being booked by another user.")
                if seat.is_booked:
                    raise Exception("Seat already booked.")
                seat_objs.append(seat)

            # Mark as booked and release locks
            for seat in seat_objs:
                seat.is_booked = True
                seat.lock.release()

            total_price = len(seat_objs) * 50  # e.g., $50 per ticket
            PaymentProcessor.process_payment(user_id, total_price, payment_method)
            booking = Booking(user_id, concert_id, [s.id for s in seat_objs], total_price)
            self.bookings.append(booking)
            user.bookings.append(booking)

            NotificationService.send_confirmation(user.email, booking.id)
            return booking
        except Exception as e:
            for seat in seat_objs:
                if seat.lock.locked():
                    seat.lock.release()
            print(f"[Error] Booking failed: {e}")
            return None

    def join_waitlist(self, user_id, concert_id):
        concert = next(c for c in self.concerts if c.id == concert_id)
        concert.waitlist.append(user_id)
        print(f"[Waitlist] User {user_id} added to waitlist for concert {concert_id}")

