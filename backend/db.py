from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()
secret_key = "giuds1kj23b21iuo3boiu21obi"


def init_db(app):
    global secret_key

    with app.app_context():
        secret_key = current_app.secret_key
