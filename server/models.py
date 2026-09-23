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

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

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

    def __repr__(self):  # how a review prints in the shell
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'
