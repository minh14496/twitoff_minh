"""
    SQLAlchemy models and database architecture
"""

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


# Creates User Table
class User(DB.Model):
    pass