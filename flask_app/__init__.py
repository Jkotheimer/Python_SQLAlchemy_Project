from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_app.sql_config import username, password

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@localhost/Company'.format(username, password)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_app import routes
from flask_app import models

