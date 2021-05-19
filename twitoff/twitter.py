"""
    Handle connection to Twitter Database
"""

from re import L
from os import getenv
from .models import DB, Tweet, User
import tweepy
import spacy


# Authenticates us and allow us to user the Twitter Authentication
TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
api = tweepy.API(TWITTER_AUTH)


# NLP model
nlp = spacy.load("my_model")


# Creating function to vectorize tweet
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Takes a username and adds them to our DB from the twitter DB.
    Get user and get up to 200 of their tweets and add to our
    SQLAlchemy database.
    """
    try:
        twitter_user = api.get_user(username)
        # Where we decide whether or not to add or update
        db_user = User.query.get(twitter_user.id) or User(
            id=twitter_user.id, username=username)

        DB.session.add(db_user)

        # TODO: grab same number of tweets for each user
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # Run vectorize_tweet function
            tweet_vector = vectorize_tweet(tweet.full_text)
            # Creating a Tweet object to add to our DB
            db_tweet = Tweet(
                id=tweet.id, text=tweet.full_text, vect=tweet_vector)
            # Connects the tweet to the user through this tweets list (user.tweets)
            db_user.tweets.append(db_tweet)
            # Note: If we added before appending we would likely get an error
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error Processing {username}: {e}")
        raise e

    else: 
        DB.session.commit()