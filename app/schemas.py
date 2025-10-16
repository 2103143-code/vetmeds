from . import ma
from marshmallow import fields, validate

class AccountSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    dob = fields.Date(required=True)
    balance = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
