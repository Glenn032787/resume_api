from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///resume.db'

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow(app)

