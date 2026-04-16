from flask import request
from flask_restful import Resource
from extensions import db
from models import Person
from schemas.person_schema import PersonSchema
from marshmallow import ValidationError

personSchema=PersonSchema()

class Signup(Resource):
    def post(self):
        data=request.get_json()

        """convert into validated python dict (validate + clean data)"""
        try:
            validated_data=personSchema.load(data)
        except ValidationError as error:
            return {'errors': error.messages}, 400


        username=validated_data.get('username')
        password=validated_data.get('password')

        
        existing_user=db.session.query(Person).filter_by(username=username).first()

        if existing_user:
            return {"error":"Username already exists!"}

        try:
            new_person=Person(username=username)
            new_person.hash_password(password)

            db.session.add(new_person)
            db.session.commit()

            return personSchema.dump(new_person), 201
        except Exception as e:
            db.session.rollback()
            print(e)
            return {'error':'user created unsucceful'},500

        



