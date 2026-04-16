from extensions import ma
from marshmallow import fields, validate


"""manual way of marshmallow validation"""
class PersonSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username=fields.String(required=True, validate=validate.Length(min=3))
    password=fields.String(required=True, load_only=True, validate=validate.Length(min=6))


# """new way marshmallow-sqlalchemy (django way)"""
# class psersonSch(SQLAlchemyAutoSchema):
#     class Meta:
#         model=Person
#         laod_instance=True
#         exclude=('password',)

#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# class AuthorSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Author
#         load_instance = True  # Optional: deseriaize to model instances
