import os

class Config:
    SECRET_KEY = "super-secret-key-change-later"
    SQLALCHEMY_DATABASE_URI = "sqlite:///lifedrop.db"   # starter DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
