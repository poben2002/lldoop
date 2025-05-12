from enum import Enum
import uuid
from datetime import datetime


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"


class PaymentMethod:
    def __init__(self, method_id, method_type):
        self.method_id = method_id
        self.method_type = method_type


class CreditCard(PaymentMethod):
    def __init__(self, card_number, expiry_date):
        super().__init__(card_number, "CreditCard")
        self.expiry_date = expiry_date


class BankAccount(PaymentMethod):
    def __init__(self, account_number, bank_name):
        super().__init__(account_number, "BankAccount")
        self.bank_name = bank_name


class Transaction:
    def __init__(self, sender_id, receiver_id, amount, currency, txn_type):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.currency = currency
        self.txn_type = txn_type  # e.g. "transfer", "deposit", "conversion"

    def __str__(self):
        return f"[{self.timestamp}] {self.txn_type.upper()} {self.amount} {self.currency.name} from {self.sender_id} to {self.receiver_id}"


class Wallet:
    def __init__(self):
        self.balances = {currency: 0.0 for currency in Currency}
        self.transactions = []

    def add_balance(self, currency, amount):
        self.balances[currency] += amount

    def deduct_balance(self, currency, amount):
        if self.balances[currency] >= amount:
            self.balances[currency] -= amount
            return True
        return False

    def get_balance(self, currency):
        return self.balances[currency]

    def record_transaction(self, txn):
        self.transactions.append(txn)

    def get_statement(self):
        return [str(txn) for txn in self.transactions]


class User:
    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.wallet = Wallet()
        self.payment_methods = []

    def add_payment_method(self, method):
        self.payment_methods.append(method)

    def remove_payment_method(self, method_id):
        self.payment_methods = [m for m in self.payment_methods if m.method_id != method_id]


class CurrencyConverter:
    exchange_rates = {
        (Currency.USD, Currency.EUR): 0.9,
        (Currency.EUR, Currency.USD): 1.1,
        (Currency.USD, Currency.JPY): 150,
        (Currency.JPY, Currency.USD): 0.0067,
        (Currency.EUR, Currency.JPY): 165,
        (Currency.JPY, Currency.EUR): 0.006,
    }

    @staticmethod
    def convert(amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        rate = CurrencyConverter.exchange_rates.get((from_currency, to_currency))
        if not rate:
            raise Exception("Unsupported currency conversion")
        return round(amount * rate, 2)


class WalletSystem:
    def __init__(self):
        self.users = {}

    def create_user(self, name, email):
        user = User(name, email)
        self.users[user.id] = user
        return user

    def transfer_funds(self, sender_id, receiver_id, amount, currency):
        sender = self.users[sender_id]
        receiver = self.users[receiver_id]
        if sender.wallet.deduct_balance(currency, amount):
            receiver.wallet.add_balance(currency, amount)
            txn = Transaction(sender_id, receiver_id, amount, currency, "transfer")
            sender.wallet.record_transaction(txn)
            receiver.wallet.record_transaction(txn)
            return True
        return False

    def deposit_funds(self, user_id, amount, currency):
        user = self.users[user_id]
        user.wallet.add_balance(currency, amount)
        txn = Transaction("external", user_id, amount, currency, "deposit")
        user.wallet.record_transaction(txn)

    def convert_currency(self, user_id, amount, from_currency, to_currency):
        user = self.users[user_id]
        if user.wallet.deduct_balance(from_currency, amount):
            converted = CurrencyConverter.convert(amount, from_currency, to_currency)
            user.wallet.add_balance(to_currency, converted)
            txn = Transaction(user_id, user_id, amount, from_currency, "conversion")
            user.wallet.record_transaction(txn)
            return True
        return False

    def get_user_statement(self, user_id):
        return self.users[user_id].wallet.get_statement()
