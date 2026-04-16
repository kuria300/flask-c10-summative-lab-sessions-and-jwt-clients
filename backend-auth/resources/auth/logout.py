from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import unset_jwt_cookies, jwt_required


class Logout(Resource):
    @jwt_required()
    def delete(self):
        response = jsonify({"message": "logout successful"})
        unset_jwt_cookies(response)

        return response
