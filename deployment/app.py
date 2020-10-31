from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from resources.books import Books, BooksList
from resources.users import Login, Users, UsersList

from db import db, init_db
from decouple import config as config_decouple
from config import config

app = Flask(__name__, static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")
environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']
app.config.from_object(environment)

init_db(app)

api = Api(app)

CORS(app, resources={r'/*': {'origins': '*'}})

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def render():
    return render_template("index.html")


api.add_resource(Books, '/book/<int:isbn>', '/book')
api.add_resource(BooksList, '/books')

api.add_resource(Users, '/user/<string:email>', '/user')
api.add_resource(UsersList, '/users')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
