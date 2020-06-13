import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '2951b9d5bb58fe1fac16d872533168aa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
if not os.path.exists('site.db'):
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskapp import routes