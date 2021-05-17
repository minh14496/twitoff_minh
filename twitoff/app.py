"""
    Main app/routing file for Twitoff
"""

from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def root():
        return render_template("base.html", title="Home")

    return app