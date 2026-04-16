from extensions import ma
from marshmallow import fields, validate


class ExpenseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    amount = fields.Decimal(as_string=True, required=True)
    description = fields.String()
    person_id = fields.Integer()
