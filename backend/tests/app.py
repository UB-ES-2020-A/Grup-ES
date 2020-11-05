from flask import Flask
from flask_migrate import Migrate

from config import config
from db import db

app = Flask(__name__)
app.config.from_object(config['test'])

migrate = Migrate(app, db)
db.init_app(app)
