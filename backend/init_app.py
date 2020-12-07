from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from resources.books import Books, BooksList, SearchBooks, BestSellers
from resources.recovery import PasswordRecovery
from resources.users import Login, Users, UsersList
from resources.library import Library, LibraryVisibility, LibraryEntry
from resources.transactions import Transactions, TransactionsUser, TransactionsList
from resources.reviews import Reviews

from db import db, init_db
from utils.mail import mail


def init_api(api):
    api.add_resource(Books, '/api/book/<int:isbn>', '/api/book')
    api.add_resource(BooksList, '/api/books')
    api.add_resource(SearchBooks, '/api/search')
    api.add_resource(BestSellers, '/api/trending')

    api.add_resource(Users, '/api/user/<string:email>', '/api/user')
    api.add_resource(UsersList, '/api/users')
    api.add_resource(Login, '/api/login')

    api.add_resource(Library, '/api/userLibrary/<string:email>')
    api.add_resource(LibraryVisibility, '/api/library/<string:email>/visibility/<string:isbn>')
    api.add_resource(LibraryEntry, '/api/library/<string:email>/<string:isbn>', '/api/library/<string:email>')

    api.add_resource(Transactions, '/api/transaction/<int:id_transaction>', '/api/transaction')
    api.add_resource(TransactionsUser, '/api/transactions/<string:email>')
    api.add_resource(TransactionsList, '/api/allTransactions')

    api.add_resource(PasswordRecovery, '/api/recovery/<string:key>', '/api/recovery')

    api.add_resource(Reviews, '/api/review', '/api/review/<int:user_id>/<int:isbn>')


def init(environment):
    app = Flask(__name__, template_folder=environment.TEMPLATE_FOLDER, static_folder=environment.STATIC_FOLDER)
    app.config.from_object(environment)

    mail.init_app(app)

    init_db(app)

    api = Api(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    migrate = Migrate(app, db)
    db.init_app(app)

    init_api(api)

    return app, api, migrate
