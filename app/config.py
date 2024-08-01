import os
from urllib.parse import quote
# URL encode your password if it contains special characters
password = 'p@stgress'
encoded_password = quote(password)



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '173120'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgress:{encoded_password}@localhost/hotel_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or '173120'