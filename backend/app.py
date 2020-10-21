from flask import Flask
from flask_cors import CORS
from flask import render_template
from flask_migrate import Migrate
from db import db
from model.users import UsersModel

app = Flask(__name__, static_folder="/home/pau/Escritorio/Grup-ES/frontend/dist/static",
         template_folder="/home/pau/Escritorio/Grup-ES/frontend/dist")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

migrate = Migrate(app, db)
db.init_app(app)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def render():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
