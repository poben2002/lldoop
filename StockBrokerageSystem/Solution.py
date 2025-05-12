import uuid
from datetime import datetime
from typing import List, Dict


# Helper Classes for Entities

class Stock:
    def __init__(self, ticker: str, name: str, price: float):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.available_quantity = 100000  # Default stock available, could be updated by market

    def update_price(self, new_price: float):
        self.price = new_price

    def __str__(self):
        return f"Stock(ticker={self.ticker}, name={self.name}, price={self.price}, available_quantity={self.available_quantity})"


class Account:
    def __init__(self, user_name: str, balance: float = 10000.0):
        self.id = uuid.uuid4()
        self.user_name = user_name
        self.balance = balance
        self.portfolio = {}  # Mapping of Stock to quantity owned
        self.transaction_history = []

    def update_balance(self, amount: float):
        self.balance += amount

    def update_portfolio(self, stock: Stock, quantity: int):
        if stock.ticker in self.portfolio:
            self.portfolio[stock.ticker] += quantity
        else:
            self.portfolio[stock.ticker] = quantity

    def __str__(self):
        return f"Account(id={self.id}, user_name={self.user_name}, balance={self.balance}, portfolio={self.portfolio})"


class Transaction:
    def __init__(self, account: Account, stock: Stock, quantity: int, price: float, transaction_type: str):
        self.id = uuid.uuid4()
        self.account = account
        self.stock = stock
        self.quantity = quantity
        self.price = price
        self.transaction_type = transaction_type
        self.transaction_date = datetime.now()
        self.total_amount = quantity * price
        self.status = "Pending"

    def execute(self):
        if self.transaction_type == "buy":
            if self.account.balance < self.total_amount:
                raise ValueError("Insufficient funds.")
            if self.stock.available_quantity < self.quantity:
                raise ValueError("Not enough stock available.")
            self.account.update_balance(-self.total_amount)
            self.stock.available_quantity -= self.quantity
            self.account.update_portfolio(self.stock, self.quantity)
        elif self.transaction_type == "sell":
            if self.account.portfolio.get(self.stock.ticker, 0) < self.quantity:
                raise ValueError("Not enough stock in portfolio.")
            self.account.update_balance(self.total_amount)
            self.stock.available_quantity += self.quantity
            self.account.update_portfolio(self.stock, -self.quantity)

        self.status = "Completed"
        self.account.transaction_history.append(self)
        return self


# Simulating the Online Stock Brokerage System

class OnlineStockBrokerageSystem:
    def __init__(self):
        self.accounts = {}
        self.stocks = {}
        self.transactions = {}

    def register_stock(self, ticker: str, name: str, price: float):
        stock = Stock(ticker, name, price)
        self.stocks[ticker] = stock
        return stock

    def register_account(self, user_name: str):
        account = Account(user_name)
        self.accounts[account.id] = account
        return account

    def view_stock_quote(self, ticker: str):
        stock = self.stocks.get(ticker)
        if stock:
            return stock.price
        return None

    def place_order(self, account_id: uuid.UUID, stock_ticker: str, quantity: int, transaction_type: str):
        account = self.accounts.get(account_id)
        stock = self.stocks.get(stock_ticker)
        
        if not account or not stock:
            raise ValueError("Account or Stock not found.")
        
        price = stock.price
        transaction = Transaction(account, stock, quantity, price, transaction_type)
        transaction.execute()
        self.transactions[transaction.id] = transaction
        return transaction

    def view_account_portfolio(self, account_id: uuid.UUID):
        account = self.accounts.get(account_id)
        if account:
            return account.portfolio
        return None

    def view_transaction_history(self, account_id: uuid.UUID):
        account = self.accounts.get(account_id)
        if account:
            return account.transaction_history
        return None

    def update_stock_price(self, ticker: str, new_price: float):
        stock = self.stocks.get(ticker)
        if stock:
            stock.update_price(new_price)
            return stock
        return None

