from flask import Flask
from flask_login import LoginManager

DEBUG = True

app = Flask(__name__)
app.secret_key = 'auoeshbouoastuhuoausoehuosthououeaauoub!'


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
# END DO NOT TOUCH HERE


from models import *
from routes import *
from forms import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    # Connect to the database before each request
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    # Disconnect from the database after each request
    g.db.close()
    return response


# @app.route('/')
# def hello_world():
#    return 'Hello World!'


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship], safe=True)
    DATABASE.close()


if __name__ == '__main__':
    import os

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
