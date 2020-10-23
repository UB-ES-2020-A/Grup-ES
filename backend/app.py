from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate

from db import db, secret_key
from model.books import BooksModel

app = Flask(__name__, static_folder="/home/pau/Escritorio/Grup-ES/frontend/dist/static",
         template_folder="/home/pau/Escritorio/Grup-ES/frontend/dist")

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def render():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
