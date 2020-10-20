from flask import Flask
from flask_cors import CORS
from flask import render_template
import os

app = Flask(__name__, static_folder="/home/pau/Escritorio/Grup-ES/frontend/dist/static",
         template_folder="/home/pau/Escritorio/Grup-ES/frontend/dist")

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def render():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
