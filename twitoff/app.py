"""Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User, Tweet


def create_app():
    """Creates and configures an instance of the flask application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)   

    @app.route('/populate')
    def populate():
        names = ["elonmusk", "jackblack"]
        messages = ["Go For Bitcoin", "Laugh", "Go for Doge", "Laugh more"
        ,"Shinu coin this time", "Laugh more and more"]
        insert_users(names)
        users = User.query.all()
        insert_tweet(tweets=messages, user=names*3)
        tweets = Tweet.query.all()
        return render_template("base.html", title="Home", users=users, tweets=tweets)

    return app


def insert_users(usernames):
    for id_index, username in enumerate(usernames):
        user = User(id=id_index, username=username)
        DB.session.add(user)
        DB.session.commit()


def insert_tweet(tweets, user):
    for index in range(6):
        tweet_ = Tweet(id=index+1, text=tweets[index], user=User.query.filter_by(username=f'{user[index]}').first())
        DB.session.add(tweet_)
        DB.session.commit()