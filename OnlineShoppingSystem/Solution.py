import uuid
from datetime import datetime
from typing import List, Dict

# Helper Classes for Entities

class Product:
    def __init__(self, name, category, price, stock_quantity):
        self.id = uuid.uuid4()
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, category={self.category}, price={self.price}, stock_quantity={self.stock_quantity})"


class User:
    def __init__(self, name, email):
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.profile = {}
        self.cart = []
        self.orders = []

    def update_profile(self, profile_info: dict):
        self.profile.update(profile_info)

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"


class Order:
    def __init__(self, user, cart, total_amount, status="Pending"):
        self.id = uuid.uuid4()
        self.user = user
        self.cart = cart
        self.total_amount = total_amount
        self.status = status
        self.order_date = datetime.now()

    def __str__(self):
        return f"Order(id={self.id}, user={self.user.name}, total_amount={self.total_amount}, status={self.status}, order_date={self.order_date})"


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self):
        return f"CartItem(product={self.product.name}, quantity={self.quantity}, total_price={self.total_price})"


# Simulating the Online Shopping System

class OnlineShoppingSystem:
    def __init__(self):
        self.products = []
        self.users = {}
        self.orders = []
    
    def register_product(self, name, category, price, stock_quantity):
        product = Product(name, category, price, stock_quantity)
        self.products.append(product)
        return product

    def register_user(self, name, email):
        user = User(name, email)
        self.users[user.id] = user
        return user

    def browse_products(self, category=None):
        if category:
            return [product for product in self.products if product.category == category]
        return self.products

    def search_product(self, search_term):
        return [product for product in self.products if search_term.lower() in product.name.lower()]

    def add_to_cart(self, user, product_id, quantity):
        product = next((p for p in self.products if p.id == product_id), None)
        if product and product.stock_quantity >= quantity:
            cart_item = CartItem(product, quantity)
            user.cart.append(cart_item)
            product.stock_quantity -= quantity
            return cart_item
        return None

    def view_cart(self, user):
        return user.cart

    def checkout(self, user):
        total_amount = sum(item.total_price for item in user.cart)
        order = Order(user, user.cart, total_amount)
        user.orders.append(order)
        self.orders.append(order)
        user.cart.clear()
        return order

    def process_payment(self, order, payment_method):
        # Simulating payment processing
        if payment_method in ["Credit Card", "Debit Card", "PayPal"]:
            order.status = "Paid"
            return order
        return None

    def track_order(self, order_id):
        return next((order for order in self.orders if order.id == order_id), None)


# Simulating the User Interaction

system = OnlineShoppingSystem()

# Register some products
product_1 = system.register_product("Smartphone", "Electronics", 500, 10)
product_2 = system.register_product("Laptop", "Electronics", 1000, 5)
product_3 = system.register_product("Headphones", "Accessories", 150, 20)
product_4 = system.register_product("Shirt", "Clothing", 30, 50)

# Register a user
user = system.register_user("John Doe", "john.doe@example.com")

# Browsing products
print("=== All Products ===")
for product in system.browse_products():
    print(product)

# Searching for a product
print("\n=== Search Results for 'Laptop' ===")
for product in system.search_product("Laptop"):
    print(product)

# Adding products to the cart
print("\n=== Adding Items to Cart ===")
cart_item_1 = system.add_to_cart(user, product_1.id, 1)
cart_item_2 = system.add_to_cart(user, product_3.id, 2)
if cart_item_1:
    print(cart_item_1)
if cart_item_2:
    print(cart_item_2)

# View Cart
print("\n=== Cart ===")
for item in system.view_cart(user):
    print(item)

# Checkout and make payment
order = system.checkout(user)
print(f"\nOrder Created: {order}")

# Processing payment
order = system.process_payment(order, "Credit Card")
if order:
    print(f"\nPayment Successful: {order}")
else:
    print("\nPayment Failed")

# Track Order
print("\n=== Track Order ===")
tracked_order = system.track_order(order.id)
if tracked_order:
    print(tracked_order)
else:
    print("Order not found.")
