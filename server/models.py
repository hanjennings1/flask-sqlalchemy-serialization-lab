from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # a customer has many reviews
    reviews = db.relationship('Review', back_populates='customer')  # pairs with Review.customer

    # shortcut: get items directly through this customer's reviews
    items = association_proxy('reviews', 'item')  # follow reviews -> each review's item

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # an item has many reviews
    reviews = db.relationship('Review', back_populates='item')  # pairs with Review.item

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


# -- REVIEW MODEL ---
# join table with comment, customer_id, and item_id
class Review(db.Model):
    __tablename__ = 'reviews'  # table name in the database

    id = db.Column(db.Integer, primary_key=True)  # unique ID for each review
    comment = db.Column(db.String)  # the review text

    # foreign keys: point to the related customer and item (use table names)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # each review belongs to one customer and one item
    customer = db.relationship('Customer', back_populates='reviews')  # pairs with Customer.reviews
    item = db.relationship('Item', back_populates='reviews')  # pairs with Item.reviews

    def __repr__(self):  # how a review prints in the shell
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'



# --- SCHEMAS (turn model objects into plain dictionaries) ---

class CustomerSchema(Schema):
    id = fields.Int()      # customer's ID
    name = fields.Str()    # customer's name

    # nested reviews, skip their customer to prevent a loop:
    reviews = fields.Nested(lambda: ReviewSchema(exclude=('customer',)), many=True)


class ItemSchema(Schema):
    id = fields.Int()       # item's ID
    name = fields.Str()     # item's name
    price = fields.Float()  # item's price (decimal number)

    # nested reviews, skip their item to prevent a loop:
    reviews = fields.Nested(lambda: ReviewSchema(exclude=('item',)), many=True)


class ReviewSchema(Schema):
    id = fields.Int()       # review's ID
    comment = fields.Str()  # review text

    # nest the related customer and item, serialized by their own schemas:
    # nested customer skips their reviews to prevent a loop:
    customer = fields.Nested(CustomerSchema(exclude=('reviews',)))
    item = fields.Nested(ItemSchema(exclude=('reviews',)))          # uses review.item, excludes reviews