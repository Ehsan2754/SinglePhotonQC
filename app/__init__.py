from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import IPAddressType


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///QantumComputingLab.db'
app.config['SECRET_KEY'] = 'w276-T#treBxTpY7X-jZZ96@tAHHtw5F'

db = SQLAlchemy(app)


DEFAULT_IMG = 'img/default.jpg'
TMP_IMG = 'img/tmp.bmp'
UNSAVED = False
SAVED = True

from app.route import dataRoute