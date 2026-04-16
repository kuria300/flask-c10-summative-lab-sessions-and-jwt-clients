from flask import request, make_response
from flask_restful import Resource
from extensions import db
from models import Person
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies
from schemas.person_schema import PersonSchema
from marshmallow import ValidationError

personSchema=PersonSchema()

class Login(Resource):
    def post(self):
        data=request.get_json()

        """convert into validated python dict (validate + clean data)"""
        try:
            validated_data=personSchema.load(data)
        except ValidationError as error:
            print(error)
            return {"errors":error.messages}, 400

        username = validated_data["username"]
        password = validated_data["password"]


        user=db.session.query(Person).filter_by(username=username).first()

        if not user:
            return {'error':'user doesn"t exist!'}, 404

        #check password 
        if not user.check_password(password):
            return {'error':'Invalid credentials'}, 400

        try:
            #create access_token
            access_token=create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            #response obj add access_token to cookie then send to frontend as httponly
            response = make_response({'message': 'login successful'})
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response
        except Exception as e:
            
            db.session.rollback()
            print(f'Errors', str(e))
            return {'error':'login failed'}, 500

