from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api

from resources.books import Books, BooksList
from resources.users import Login, Users, UsersList
from resources.library import Library
from resources.transactions import Transactions


from db import db, init_db


def init_api(api):
    api.add_resource(Books, '/book/<int:isbn>', '/book')
    api.add_resource(BooksList, '/books')

    api.add_resource(Users, '/user/<string:email>', '/user')
    api.add_resource(UsersList, '/users')
    api.add_resource(Login, '/login')

    api.add_resource(Library, '/library/<string:email>', '/library')

    api.add_resource(Transactions, '/transaction/<int:id_transaction>', '/transaction')


def init(environment):
    app = Flask(__name__, template_folder=environment.TEMPLATE_FOLDER, static_folder=environment.STATIC_FOLDER)
    app.config.from_object(environment)

    mail = Mail(app)

    init_db(app)

    api = Api(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    migrate = Migrate(app, db)
    db.init_app(app)

    init_api(api)

    return app, api, migrate, mail
