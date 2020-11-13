from flask import render_template
from decouple import config as config_decouple

from config import config
from init_app import init

environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']
app, api, migrate = init(environment)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


api.add_resource(Books, '/book/<int:isbn>', '/book')

api.add_resource(Users, '/user/<string:email>', '/user')
api.add_resource(UsersList, '/users')
api.add_resource(BooksList, '/books')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000)
