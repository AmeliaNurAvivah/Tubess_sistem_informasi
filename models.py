from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(255), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')

    def __init__(self, items, customer_name, customer_phone, customer_address):
        self.items = items
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_address = customer_address

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

    def clear(self):
        self.items = []
