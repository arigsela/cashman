import datetime as dt

# Library for object serialization (ORM) converting objects to python datatypes
from marshmallow import Schema, fields

class Transaction(object):
    def __init__(self, description, amount, type):
        self.description = description
        self.amount = amount
        self.created_at = dt.datetime.now()
        self.type = type

    # return string representation of an object
    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)
    
# Schema for serialization
class TransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    created_at = fields.Date()
    type = fields.Str()

