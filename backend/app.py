from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate

from db import db, secret_key
from resources.users import Login, Users, UsersList

app = Flask(__name__, static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")

app.config.from_object(__name__)
api = Api(app)

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def render():
    return render_template("index.html")


api.add_resource(Users, '/user/<string:email>', '/user')
api.add_resource(UsersList, '/users')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
