from flask import render_template
from decouple import config as config_decouple

from config import config
from init_app import init

environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']
app, api, migrate = init(environment)


@app.route('/')
def render():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
