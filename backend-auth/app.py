from flask import Flask, jsonify
from config import Config
from flask_restful import Api
from extensions import db, migrate, bcrypt, jwt, ma
from resources.auth.signup import Signup
from resources.home import Home
from resources.auth.login import Login
from resources.expenses.resource_list import Access_res
from resources.expenses.expense_detail import Expensedetail
from resources.auth.refresh_tkn import TokenRefresh
from resources.auth.logout import Logout
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app=Flask(__name__)
app.config.from_object(Config)

api=Api(app)
CORS(app, origins=["http://localhost:4000"])

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)
ma.init_app(app)

#missing
@jwt.unauthorized_loader
def missing_token_callback(reason):
    return jsonify({
        "message": "You must log in to access this resource"
    }), 401
#invalid
@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return jsonify({
        "error": "invalid_token",
        "message": "Token is invalid or malformed"
    }), 422
#expired
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": "token_expired",
        "message": "Your session has expired. Please log in again"
    }), 401

api.add_resource(Signup, '/auth/signup')
api.add_resource(Home, '/')
api.add_resource(Login, '/auth/login')
#protected_route
api.add_resource(Logout, '/api/auth/logout')
api.add_resource(Access_res, '/api/resource')
api.add_resource(Expensedetail, '/api/resource/<int:id>')
api.add_resource(TokenRefresh, '/token/refresh')



if __name__== "__main__":
    app.run(port=5001)
