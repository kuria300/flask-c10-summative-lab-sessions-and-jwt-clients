import os

class Config:
    """application metadata"""
    DEBUG=True

    SQLALCHEMY_DATABASE_URI= "sqlite:///db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """"jwt config"""
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_SECRET_KEY= os.getenv('SECRET_KEY')
    JWT_ACCESS_COOKIE_PATH = "/api/"
    JWT_ACCESS_CSRF_COOKIE_PATH = "/api/"
    JWT_REFRESH_COOKIE_PATH= "/token/refresh"

    # JWT_COOKIE_SECURE
    # JWT_COOKIE_SAMESITE

    #x-csrf-token : 6bf5dca8-3b86-4abd-aca8-95a97595f3dc  
    #even for refresh-token
    # a key-val pair needed when deleting its been checked in postman add in headers manually 
    #if not JWT_COOKIE_CSRF_PROTECT = False   will not be enforced in logout