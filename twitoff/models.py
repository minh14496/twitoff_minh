"""SQLAlchemy models and database architecture"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# Creates a 'user' Table
class User(DB.Model):
    # id primary key column for 'user'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column for 'user'
    username = DB.Column(DB.String, nullable=False)
     # stores most recent tweet_id
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self): # this is called representation of a class
        return f"<User: {self.username}>"


# Creates a 'tweet' Table
class Tweet(DB.Model):
    # id primary key column for 'tweet'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column for 'tweet'
    text = DB.Column(DB.Unicode(350))
    # stores numbers that represents tweets
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id foreign key column for 'tweet'
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)

    ### TODO: STRETCH GOAL ###
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self): # this is called representation of a class
        return f"<Tweet: {self.text}>"