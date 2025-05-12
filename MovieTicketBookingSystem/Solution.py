import uuid
from datetime import datetime
from typing import List, Dict

# Helper Classes for the Entities

class Movie:
    def __init__(self, title, genre, duration_mins, language):
        self.id = uuid.uuid4()
        self.title = title
        self.genre = genre
        self.duration_mins = duration_mins
        self.language = language

    def __str__(self):
        return f"Movie(id={self.id}, title={self.title}, genre={self.genre}, language={self.language})"


class Theater:
    def __init__(self, name, city, address):
        self.id = uuid.uuid4()
        self.name = name
        self.city = city
        self.address = address
        self.screens = []

    def add_screen(self, screen):
        self.screens.append(screen)

    def __str__(self):
        return f"Theater(id={self.id}, name={self.name}, city={self.city})"


class Screen:
    def __init__(self, name, rows, seats_per_row):
        self.id = uuid.uuid4()
        self.name = name
        self.seating_layout = self.generate_seating_layout(rows, seats_per_row)

    def generate_seating_layout(self, rows, seats_per_row):
        layout = {}
        for row in range(1, rows + 1):
            for seat in range(1, seats_per_row + 1):
                layout[f"{chr(64+row)}{seat}"] = "available"
        return layout

    def __str__(self):
        return f"Screen(id={self.id}, name={self.name})"


class Show:
    def __init__(self, movie, screen, start_time, price_by_seat_type):
        self.id = uuid.uuid4()
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        self.price_by_seat_type = price_by_seat_type
        self.seat_status = screen.seating_layout.copy()

    def __str__(self):
        return f"Show(id={self.id}, movie={self.movie.title}, start_time={self.start_time}, screen={self.screen.name})"


class Booking:
    def __init__(self, user_id, show, selected_seats, total_amount):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.show = show
        self.selected_seats = selected_seats
        self.total_amount = total_amount
        self.status = 'pending'
        self.payment_id = None

    def confirm_payment(self, payment_id):
        self.payment_id = payment_id
        self.status = 'confirmed'
        for seat in self.selected_seats:
            self.show.seat_status[seat] = "booked"

    def __str__(self):
        return f"Booking(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount}, status={self.status})"


# Simulating User Flow

class MovieTicketBookingSystem:
    def __init__(self):
        self.movies = []
        self.theaters = []
        self.users = {}
        self.bookings = []
        self.payments = {}
    
    def register_movie(self, title, genre, duration_mins, language):
        movie = Movie(title, genre, duration_mins, language)
        self.movies.append(movie)
        return movie

    def register_theater(self, name, city, address):
        theater = Theater(name, city, address)
        self.theaters.append(theater)
        return theater

    def create_show(self, movie, theater, start_time, price_by_seat_type):
        screen = Screen(name=f"Screen {len(theater.screens)+1}", rows=5, seats_per_row=10)
        theater.add_screen(screen)
        show = Show(movie, screen, start_time, price_by_seat_type)
        return show

    def browse_movies(self):
        return self.movies

    def browse_shows(self, movie_id):
        shows = []
        for theater in self.theaters:
            for screen in theater.screens:
                for show in screen.seating_layout:
                    if show.movie.id == movie_id:
                        shows.append(show)
        return shows

    def book_seats(self, user_id, show, seats):
        total_amount = sum([show.price_by_seat_type[show.seat_status[seat]] for seat in seats])
        booking = Booking(user_id, show, seats, total_amount)
        self.bookings.append(booking)
        return booking

    def make_payment(self, booking_id, payment_id):
        booking = next(b for b in self.bookings if b.id == booking_id)
        booking.confirm_payment(payment_id)
        return booking


# Simulating the User Interaction

system = MovieTicketBookingSystem()

# Register movies
movie_1 = system.register_movie("Avengers: Endgame", "Action", 180, "English")
movie_2 = system.register_movie("The Lion King", "Animation", 118, "English")

# Register theaters
theater_1 = system.register_theater("Cineplex", "New York", "5th Ave, NY")
theater_2 = system.register_theater("PVR", "Los Angeles", "Sunset Blvd, LA")

# Create shows for movies
show_1 = system.create_show(movie_1, theater_1, datetime(2023, 6, 15, 19, 30), {"normal": 10.0, "premium": 20.0})
show_2 = system.create_show(movie_2, theater_2, datetime(2023, 6, 16, 14, 00), {"normal": 8.0, "premium": 16.0})

# User flow
print("=== Available Movies ===")
for movie in system.browse_movies():
    print(movie)

print("\n=== Available Shows for 'Avengers: Endgame' ===")
for show in system.browse_shows(movie_1.id):
    print(show)

# User selects show and books seats
user_id = uuid.uuid4()  # Simulating a new user
selected_seats = ["A1", "A2", "A3"]  # Simulated selected seats
booking = system.book_seats(user_id, show_1, selected_seats)
print(f"\nBooking Created: {booking}")

# User makes payment
payment_id = uuid.uuid4()  # Simulating a payment
confirmed_booking = system.make_payment(booking.id, payment_id)
print(f"\nConfirmed Booking: {confirmed_booking}")
