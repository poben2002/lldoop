from datetime import datetime, timedelta
import uuid


class Book:
    def __init__(self, title, author, isbn, publication_year):
        self.id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"


class Member:
    def __init__(self, name, contact_info):
        self.id = str(uuid.uuid4())
        self.name = name
        self.contact_info = contact_info
        self.borrowed_books = []  # list of Loan objects

    def has_overdue_books(self):
        now = datetime.now()
        return any(loan.return_date is None and loan.due_date < now for loan in self.borrowed_books)


class Loan:
    def __init__(self, book, member, loan_period_days=14):
        self.id = str(uuid.uuid4())
        self.book = book
        self.member = member
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=loan_period_days)
        self.return_date = None

    def mark_returned(self):
        self.return_date = datetime.now()


class Librarian:
    def __init__(self, name):
        self.name = name

    def add_book(self, system, title, author, isbn, year):
        book = Book(title, author, isbn, year)
        system.books[book.id] = book
        return book

    def remove_book(self, system, book_id):
        if book_id in system.books and system.books[book_id].is_available:
            del system.books[book_id]
            return True
        return False

    def update_book(self, system, book_id, **kwargs):
        book = system.books.get(book_id)
        if not book:
            return False
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        return True


class LibrarySystem:
    MAX_BORROW_LIMIT = 5
    LOAN_DURATION_DAYS = 14

    def __init__(self):
        self.books = {}     # book_id -> Book
        self.members = {}   # member_id -> Member
        self.loans = {}     # loan_id -> Loan

    def register_member(self, name, contact_info):
        member = Member(name, contact_info)
        self.members[member.id] = member
        return member

    def borrow_book(self, member_id, book_id):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book or not book.is_available:
            return None

        if len([l for l in member.borrowed_books if l.return_date is None]) >= self.MAX_BORROW_LIMIT:
            return None

        loan = Loan(book, member, self.LOAN_DURATION_DAYS)
        member.borrowed_books.append(loan)
        self.loans[loan.id] = loan
        book.is_available = False
        return loan

    def return_book(self, member_id, book_id):
        member = self.members.get(member_id)
        book = self.books.get(book_id)
        if not member or not book:
            return False

        for loan in member.borrowed_books:
            if loan.book.id == book_id and loan.return_date is None:
                loan.mark_returned()
                book.is_available = True
                return True
        return False

    def get_borrowed_books(self, member_id):
        member = self.members.get(member_id)
        return [loan for loan in member.borrowed_books if loan.return_date is None] if member else []
