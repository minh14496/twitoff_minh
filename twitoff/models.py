"""
    SQLAlchemy models and database architecture
"""

from flask.helpers import get_template_attribute
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


# Creates a User Table
class User(DB.Model):
    # id primary key column for 'user'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column for 'user'
    username = DB.Column(DB.String, nullable=False)

    def __repr__(self): # this is called a representation
        return r"<User: {self.username}>"


# Creates a Tweet Table
class Tweet(DB.Model):
    # id primary key column for 'tweet'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # test col for 'tweet'
    text = DB.Column(DB.Unicode(300))
    # user_id foreign key col for 'tweet'
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    ### TODO: STRETCH GOAL ###
    # Back reference 
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self): # this is called a representation
        return r'<Tweet: {self.text}>'