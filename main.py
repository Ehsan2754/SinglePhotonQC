import time, os, json
import src
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api,Resource
# ----------- Global Variables
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app)
DEFAULT_IMG = 'img/default.jpg'
TMP_IMG = 'img/tmp.bmp'
UNSAVED = False
SAVED = True


# ----------- BOT-ACTIVATION
# ----------- Classes
class History(db.Model):
    # --- TEMPERORAY STATUS IN DB
    status = UNSAVED
    # identification
    id = db.Column(db.Integer, primary_key=True)
    # --- destination SLM
    dest = db.Column(db.String(15), nullable=True)
    # --- Gaussian waist
    gussianWaist = db.Column(db.Float, nullable=False)
    # --- Number of parameters for LG
    nValues = db.Column(db.Integer, nullable=False)
    # --- values for LG parameters
    values = db.relationship('Values', backref='owner')
    # --- Scanning position
    scanPos = db.Column(db.Integer, nullable=False)
    # --- Scanning range
    scanRange = db.Column(db.Integer, nullable=False)
    # --- Creation Date
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # TO-DO :
    # add the scanning parameters(x,y)
    # image
    # loading option
    def __repr__(self):
        return '''
        <{0}>
        <{1}>
        <{2}>
        <{3}>
        <{4}>
        <{5}>
        <{6}>
        <{7}>
        '''.format(self.id,self.date,self.dest,self.gussianWaist,self.scanPos,self.scanRange,str(self.nValues),self.values)


class Values(db.Model):
    status = UNSAVED
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'))
    coefficient = db.Column(db.Float, nullable=False)
    parameter = db.Column(db.Float, nullable=False)
    index = db.Column(db.Integer,nullable=False)


    def __repr__(self):
        return '<i={},p={},c={}>'.format(self.index, self.parameter, self.coefficient)


# ----------- Constants
INIT_form = History(id=0,
                    gussianWaist=None,
                    nValues=1,
                    values=[Values(parameter=None, coefficient=None)],
                    scanPos=None,
                    scanRange=None)
TMP_history = History()
TMP_values = []
# ----------- REST-FUL API SERVICE
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'post'
    else:
        history = History.query.order_by(History.date).all()
        print(history)
        return render_template('dashboard.html',
                               history=history,
                               preload=INIT_form,
                               path=url_for('static', filename=DEFAULT_IMG),
                               devices=src.getDevices())


@app.route('/plot', methods=['POST'])
def plot():
    form = request.form
    content={}
    for item in form:
        content[item] = form[item]
    TMP_values.clear()
    TMP_history = History(
                gussianWaist=float(content['w']),
                nValues=int(content['nLG']),
                scanPos=int(content['ScPo']),
                scanRange=int(content['ScRa']),
                status=UNSAVED
                )
    for i in range(int(content['nLG'])):
        TMP_values.append(
            Values(
                index = int(i+1)
            ,
                coefficient=float(content.pop('C{}'.format(i + 1)))
            ,
                parameter=float(content.pop('LG{}'.format(i + 1)))
            ,
                owner=TMP_history
            )           
        )
    print(TMP_history)
    history = History.query.order_by(History.date).all()
    # return str(TMP_history)
    return render_template('dashboard.html',
                               history=history,
                               preload=TMP_history,
                               path=url_for('static', filename=TMP_IMG),
                               devices=src.getDevices())


@app.route('/slm', methods=['POST'])
def slm():
    return request.form


@app.route('/refreshSLM')
def refreshSLM():
    return 'refreshSLM'


@app.route('/ack', methods=['GET'])
def acknowledge():
    return {'msg': 'Server OK'}


# ----------- MAIN
if __name__ == "__main__":
    src.welcome()
    # print(os.system(src.TUNNEL_CMD))
    # input('#### PRESS ANY KEY ####')
    app.run(debug=True)
    # try:
    # except Exception as ex:
    #     print('\t >> ERR: ' + ex)
