from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity


class TokenRefresh(Resource):
    @jwt_required(refresh=True) # looks for the 'refresh_token_cookie'
    def post(self):
        current_user = get_jwt_identity()
        
        # 2. Create the response
        response = jsonify({'refresh': 'new access_token created'}, 200)
        
        # 3. Create a NEW Access Cookie
        new_access_token = create_access_token(identity=current_user)
        set_access_cookies(response, new_access_token)
        
        return response