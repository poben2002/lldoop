import uuid
from datetime import datetime
from collections import defaultdict

class Customer:
    def __init__(self, name, contact):
        self.id = str(uuid.uuid4())
        self.name = name
        self.contact = contact
        self.orders = []
        self.reservations = []

    def place_order(self, system, items):
        order = system.create_order(self.id, items)
        self.orders.append(order)
        return order

    def make_reservation(self, system, datetime_slot, people_count):
        res_id = str(uuid.uuid4())
        reservation = {
            "id": res_id,
            "customer_id": self.id,
            "time": datetime_slot,
            "people": people_count
        }
        self.reservations.append(reservation)
        system.reservations.append(reservation)
        return reservation


class MenuItem:
    def __init__(self, name, price, ingredients):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.ingredients = ingredients  # List of ingredient names


class InventoryItem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity  # in units

    def use(self, amount):
        if self.quantity < amount:
            raise Exception(f"Not enough {self.name} in inventory.")
        self.quantity -= amount


class Order:
    def __init__(self, customer_id, items):
        self.id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.items = items  # list of MenuItem
        self.timestamp = datetime.now()
        self.status = "pending"
        self.total = sum(item.price for item in items)

    def mark_prepared(self):
        self.status = "prepared"

    def mark_paid(self):
        self.status = "completed"


class Payment:
    def __init__(self, method, amount):
        self.id = str(uuid.uuid4())
        self.method = method  # 'cash', 'card', 'mobile'
        self.amount = amount
        self.timestamp = datetime.now()


class Staff:
    def __init__(self, name, role):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role  # e.g., Chef, Waiter
        self.schedule = []
        self.performance = []

    def log_shift(self, shift_time):
        self.schedule.append(shift_time)

    def record_performance(self, note):
        self.performance.append(note)


class RestaurantSystem:
    def __init__(self):
        self.customers = {}
        self.menu = []
        self.inventory = {}
        self.orders = []
        self.reservations = []
        self.staff_members = []
        self.sales = []

    # ----- Customer Handling -----
    def register_customer(self, name, contact):
        customer = Customer(name, contact)
        self.customers[customer.id] = customer
        return customer

    # ----- Menu Management -----
    def add_menu_item(self, name, price, ingredients):
        item = MenuItem(name, price, ingredients)
        self.menu.append(item)
        return item

    def get_menu(self):
        return self.menu

    # ----- Inventory Management -----
    def add_inventory_item(self, name, quantity):
        if name in self.inventory:
            self.inventory[name].quantity += quantity
        else:
            self.inventory[name] = InventoryItem(name, quantity)

    def check_inventory(self):
        return self.inventory

    # ----- Orders -----
    def create_order(self, customer_id, item_ids):
        items = [item for item in self.menu if item.id in item_ids]
        for item in items:
            for ingredient in item.ingredients:
                self.inventory[ingredient].use(1)  # Simplified consumption logic
        order = Order(customer_id, items)
        self.orders.append(order)
        return order

    # ----- Payment -----
    def process_payment(self, order_id, method):
        order = next(o for o in self.orders if o.id == order_id)
        if order.status != "prepared":
            raise Exception("Order not ready for payment.")
        payment = Payment(method, order.total)
        order.mark_paid()
        self.sales.append(payment)
        return payment

    # ----- Staff Management -----
    def add_staff_member(self, name, role):
        staff = Staff(name, role)
        self.staff_members.append(staff)
        return staff

    def get_staff_schedule(self):
        return [(s.name, s.schedule) for s in self.staff_members]

    # ----- Reporting -----
    def generate_sales_report(self):
        total = sum(p.amount for p in self.sales)
        return {"total_sales": total, "num_transactions": len(self.sales)}

    def generate_inventory_report(self):
        return {name: item.quantity for name, item in self.inventory.items()}
