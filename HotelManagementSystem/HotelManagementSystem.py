from enum import Enum
from datetime import date


class RoomType(Enum):
    SINGLE = "Single"
    DOUBLE = "Double"
    DELUXE = "Deluxe"
    SUITE = "Suite"


class Room:
    def __init__(self, room_number, room_type: RoomType, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_available = True

    def __str__(self):
        return f"{self.room_type.value} Room #{self.room_number} - ${self.price}/night"


class Guest:
    def __init__(self, name, contact, id_number):
        self.name = name
        self.contact = contact
        self.id_number = id_number

    def __str__(self):
        return f"{self.name} (ID: {self.id_number})"


class ReservationStatus(Enum):
    BOOKED = "Booked"
    CHECKED_IN = "Checked-In"
    CHECKED_OUT = "Checked-Out"
    CANCELLED = "Cancelled"


class Reservation:
    _id_counter = 1

    def __init__(self, guest, room, check_in, check_out):
        self.id = Reservation._id_counter
        Reservation._id_counter += 1

        self.guest = guest
        self.room = room
        self.check_in_date = check_in
        self.check_out_date = check_out
        self.status = ReservationStatus.BOOKED

    def __str__(self):
        return f"Reservation #{self.id} for {self.guest.name} in Room {self.room.room_number} ({self.status.value})"


class PaymentMethod(Enum):
    CASH = "Cash"
    CARD = "Credit Card"
    ONLINE = "Online Payment"


class Payment:
    def __init__(self, reservation, amount, method: PaymentMethod):
        self.reservation = reservation
        self.amount = amount
        self.method = method
        self.success = False

    def process(self):
        # Dummy logic
        self.success = True
        return self.success


class HotelManagementSystem:
    def __init__(self):
        self.rooms = []
        self.guests = []
        self.reservations = []

    def add_room(self, room):
        self.rooms.append(room)

    def add_guest(self, guest):
        self.guests.append(guest)

    def find_available_room(self, room_type):
        for room in self.rooms:
            if room.room_type == room_type and room.is_available:
                return room
        return None

    def book_room(self, guest, room_type, check_in, check_out):
        room = self.find_available_room(room_type)
        if not room:
            print(f"No available {room_type.value} rooms.")
            return None

        reservation = Reservation(guest, room, check_in, check_out)
        self.reservations.append(reservation)
        room.is_available = False
        print(f"Booked: {reservation}")
        return reservation

    def check_in(self, reservation_id):
        for r in self.reservations:
            if r.id == reservation_id and r.status == ReservationStatus.BOOKED:
                r.status = ReservationStatus.CHECKED_IN
                print(f"Checked in: {r}")
                return True
        return False

    def check_out(self, reservation_id):
        for r in self.reservations:
            if r.id == reservation_id and r.status == ReservationStatus.CHECKED_IN:
                r.status = ReservationStatus.CHECKED_OUT
                r.room.is_available = True
                payment = Payment(r, (r.check_out_date - r.check_in_date).days * r.room.price, PaymentMethod.CARD)
                payment.process()
                print(f"Checked out: {r} | Payment of ${payment.amount} processed.")
                return True
        return False
