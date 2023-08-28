from marshmallow import post_load
from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType

class Income(Transaction):
    def __init__(self, description, amount):
        super(Income, self).__init__(description, amount, TransactionType.INCOME)

    def __repr__(self):
        return '<Income(name={self.description!r})>'.format(self=self)

class IncomeSchema(TransactionSchema):
    # this is used to deserialize an object
    @post_load
    # kwargs its variable length argument list
    def make_income(self, data, **kwargs):
        # Pass multiple arguments to the income init function
        return Income(**data)