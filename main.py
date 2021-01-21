import time, os, json, threading as td, cmd
from datetime import datetime
from cmd import welcome
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api,Resource
# ----------- Global Variables
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app)


# ----------- BOT-ACTIVATION
# ----------- Classes
class History(db.Model):
    # identification
    id = db.Column(db.Integer, primary_key=True)
    # --- destination SLM
    dest = db.Column(db.String(15), nullable=False)
    # --- Number of parameters for LG
    nValues = db.Column(db.Float, nullable=False)
    # --- values for LG parameters
    values = db.relationship('Values', backref='owner')
    # --- Creation Date
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # TO-DO :
    # add the scanning parameters(x,y)
    # image
    # loading option 
    def __repr__(self):
        return '+<{}><{}><{}><{}>'.format(self.id, self.dest, self.date,self.values)


class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
    coefficient = db.Column(db.Float, nullable=False)
    parameter = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return '<p={}c={}>:'.format(self.parameter, self.coefficient)
  

# ----------- REST-FUL API SERVICE
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'post'
    else:
        history = History.query.order_by(History.date).all()
        print(history)
        return render_template('dashboard.html',history=history,i=4)


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
    # print(os.system(cmd.TUNNEL_CMD))
    # input('#### PRESS ANY KEY ####')
    app.run(debug=True)
    # try:
    # except Exception as ex:
    #     print('\t >> ERR: ' + ex)
