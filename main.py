import time, os, json, threading as td, cmd
from datetime import datetime
from cmd import welcome
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api,Resource
# ----------- Global Variables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app)


# ----------- BOT-ACTIVATION
# ----------- Classes
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dest = db.Column(db.String(15), nullable=False)
    nValues = db.Column(db.Integer, nullable=False)
    values = db.relationship('Values', backref='owner')
    date = datetime.utcnow

    def __str__(self):
        return '+<{}><{}><{}><{}>'.format(self.id, self.dest, self.date,values)


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
    coefficient = db.Column(db.Integer, nullable=False)
    parameter = db.Column(db.Integer, nullable=False)


# ----------- REST-FUL API SERVICE
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'post'
    else:
        history = History.query.order_by(History.date).all()
        print(history)
        return render_template('dashboard.html',history=history)


@app.route('/plot', methods=['POST'])
def plot():
    return 'plot'


@app.route('/slm', methods=['POST'])
def slm():
    return 'slm'


@app.route('/refreshSLM')
def refreshSLM():
    return 'refreshSLM'


@app.route('/ack', methods=['GET'])
def acknowledge():
    return {'msg': 'Server OK'}


# ----------- MAIN
if __name__ == "__main__":
    welcome()
    print(os.system(cmd.TUNNEL_CMD))
    # input('#### PRESS ANY KEY ####')
    try:
        app.run(debug=True)
    except Exception as ex:
        print('\t >> ERR: ' + ex)
