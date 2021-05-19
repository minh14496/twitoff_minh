"""Main app/routing file for Twitoff"""

from flask import Flask, render_template, request
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user


def create_app():
    """Creates and configures an instance of the flask application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def root():
        # tweets = Tweet.query.all()
        if request.method == "POST":
            username = request.form.get("user")
            add_or_update_user(username)
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/reset', methods=["GET", "POST"])
    def reset():
        DB.drop_all()
        DB.create_all()
        # tweets = Tweet.query.all()
        return render_template("base.html", title="Home", users=User.query.all())  

    @app.route('/user/<name>')
    def user_name(name):
        # a simple version of pulling user from local DB
        user = User.query.filter_by(username=f'{name}').first()
        return render_template("user.html", title="Tweets", user=user)


    @app.route('/populate')
    def populate():
        # names = ["Elon Musk", "Jack Black"]
        # messages = ["Go For Bitcoin", "Laugh", "Go for Doge", "Laugh more"
        # ,"Shinu coin this time", "Laugh more and more"]
        # insert_users(names)
        # insert_tweet(tweets=messages, user=names*3)
        # tweets = Tweet.query.all()
        add_or_update_user("elonmusk")
        add_or_update_user("jackblack")
        return render_template("base.html", title="Home", users=User.query.all())

    return app


# def insert_users(usernames):
#     for id_index, username in enumerate(usernames):
#         user = User(id=id_index, username=username)
#         DB.session.add(user)
#         DB.session.commit()


# def insert_tweet(tweets, user):
#     for index in range(6):
#         tweet_ = Tweet(id=index+1, text=tweets[index], user=User.query.filter_by(username=f'{user[index]}').first())
#         DB.session.add(tweet_)
#         DB.session.commit()