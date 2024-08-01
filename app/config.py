from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:p@stgress@localhost:5433/hotel_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '173120'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
