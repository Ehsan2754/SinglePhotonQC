import time, os, json, base64
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect,session
from flask_ngrok import run_with_ngrok
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from math import factorial
from scipy.special import assoc_laguerre as lg
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.figure import Figure
import src
# from flask_restful import Api,Resource
# ----------- Global Variables
app = Flask(__name__)
run_with_ngrok(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///QantumComputingLab.db'
app.config['SECRET_KEY'] = 'w276-T#treBxTpY7X-jZZ96@tAHHtw5F'
db = SQLAlchemy(app)
DEFAULT_IMG = 'img/default.jpg'
TMP_IMG = 'img/tmp.bmp'
UNSAVED = False
SAVED = True


# ----------- BOT-ACTIVATION
# ----------- Classes
class Superposition(db.Model):

    ### DATABASE attributes
    __tablename__ = 'Superposition'
    # Identification
    id = db.Column(db.Integer, primary_key=True)
    # --- Destination SLM
    destination = db.relationship('Devices', backref='Superposition')
    # --- Height
    height = db.Column(db.Integer, nullable=False)
    # --- Width
    width  = db.Column(db.Integer, nullable=False)
    # --- Gaussian waist "W"
    gussian_waist = db.Column(db.Float, nullable=False)
    # --- Radial Index
    radial_index = db.Column(db.Float, nullable=False)
    # --- Number of parameters for LG
    n_values = db.Column(db.Integer, nullable=False)
    # --- Values for LG parameters
    values = db.relationship('LG_Values', backref='Superposition')
    # --- Scanning position
    h_shift = db.Column(db.Integer, nullable=False)
    # --- Scanning range
    v_shift = db.Column(db.Integer, nullable=False)
    # --- Blaze Period
    blaze_period = db.Column(db.Float)
    # --- Image file
    image = db.Column(db.LargeBinary)
    # --- Creation date
    date = db.Column(db.DateTime, default=datetime.utcnow)


    # TO-DO :
    # add the scanning parameters(x,y)
    # image
    # loading option
    def __repr__(self):
        return f'''
        <{id}>
        <{destination.id}>
        <{gussian_waist}>
        <{radial_index}>
        <{n_values}>
        <{values}>
        <{h_shift}>
        <{v_shift}>
        <{blaze_period}>
        <{date}>
        '''

    def get_LG_pairs(self,values=self.values):
        buffer = {t.index:(t.parameter,t.coefficient) for t in values}
        buffer_s = {k: buffer[k] for k in sorted(buffer)}
        return [buffer_s[i] for i in buffer_s]

    def getAxis(self,magnitute,shift):
        return np.linspace(-1*magnitute/2+shift,magnitute/2+shift-1,magnitute)

    def car2polar(self,x,y):
        rho = np.hypot(x,y)
        phi = np.arctan2(y, x)
        return rho, phi

    def Lpl(self, x,l,p):
        value = 0
        for i in range(p+1):
            value = value+((-1)**(i))*factorial(p+abs(l))/factorial(p-i)/factorial(abs(l)+i)/factorial(i)*x**i
        return value

    def N_PL(self,p,l):
        return np.sqrt(factorial(p)/factorial(p+abs(l)))

    def lagurrelGussian(self,rho,phi,w,l,p):
        rho2w = rho/w
        return N_PL(p,l)*np.power(np.sqrt(2)*rho2w,abs(l))*lg(2*np.power(rho2w,2),p,abs(l))*np.exp(-1*np.power(rho2w,2))*np.exp(complex(0,-1)*l*phi)

    def get_Superposition(self,width=self.width,height=self.height,h_shift=self.h_shift,v_shift=self.v_shift,w=self.gussian_waist,p=self.radial_index,values=self.get_LG_pairs()):
        x, y     = getAxis(width,h_shift),getAxis(height,v_shift)
        xv, yv   = np.meshgrid(x,y)
        rho, phi = car2polar(xv,yv)
        out  = 0
        for m,n in values:
            temp = n*lagurrelGussian(rho,phi,w,m,p)
            out += temp  
        return out 
        
    
    def get_Superposition_image(self,width=self.width,height=self.height,h_shift=self.h_shift,v_shift=self.v_shift,w=self.gussian_waist,p=self.radial_index,values=self.get_LG_pairs(),ri=self.radial_index,scale=255):
        out = self.get_Superposition(width,height,h_shift,v_shift,w,p,values)
        x, y     = getAxis(width,h_shift),getAxis(height,v_shift)
        xv, yv   = np.meshgrid(x,y)
        amp   = np.absolute(out)
        phase = np.angle(out)
        amp=amp/np.amax(amp)
        phase_mod = (phase+2*np.pi*xv/ri) % (2*np.pi)   
        result = amp*phase_mod
        scaled_result = result/result.max()*scale
        buf = BytesIO()
        plt.imsave(buf,scaled_result, cmap="gray",origin='lower', vmin = 0,vmax=scale,format="png")
        return base64.b64encode(buf.getbuffer()).decode("ascii")

class Devices(db.Model):
    __tablename__ = 'Devices'
    id = db.Column(db.Integer, primary_key=True)
    Superposition_id = Column(Integer, ForeignKey('Superposition.id'))
    

class LG_Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Superposition_id = db.Column(db.Integer, db.ForeignKey('Superposition.id'))
    index = db.Column(db.Integer, nullable=False)
    coefficient = db.Column(db.Float, nullable=False)
    parameter = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return '<i={},p={},c={}>'.format(self.index, self.parameter,
                                         self.coefficient)
# ----------- Constants
INIT_form = Superposition(id=0,
                    gussianWaist=None,
                    nValues=1,
                    values=[Values(parameter=None, coefficient=None)],
                    scanPos=None,
                    scanRange=None,
                    image=src.getB64string(
                        open('static/img/default.jpg', 'rb').read()))
TMP_SP = Superposition()
TMP_values = []


# ----------- REST-FUL API SERVICE
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'post'
    else:
        history = History.query.order_by(History.date).all()
        print(history)
        # Clear the TMP image
        return render_template('dashboard.html',
                               user = 'Ethan',
                               history=history,
                               preload=INIT_form,
                               devices=src.getDevices())


@app.route('/plot', methods=['POST'])
def plot():
    form = request.form
    content = {}
    for item in form:
        content[item] = form[item]
    global TMP_history
    global TMP_values
    TMP_values.clear()
    TMP_history = History(gussianWaist=float(content['w']),
                          nValues=int(content['nLG']),
                          scanPos=int(content['ScPo']),
                          scanRange=int(content['ScRa']),
                          status=UNSAVED)
    for i in range(int(content['nLG'])):
        TMP_values.append(
            Values(index=int(i + 1),
                   coefficient=float(content.pop('C{}'.format(i + 1))),
                   parameter=float(content.pop('LG{}'.format(i + 1))),
                   owner=TMP_history,
                   status=UNSAVED))
    # TODO:
    # *Image Creation
    TMP_history.processImage()
    print(TMP_history)
    history = History.query.order_by(History.date).all()
    # TODO :
    # IMAGE STRUCTURE
    # REDIRECTION
    # BASE64 format or BMP
    return render_template('dashboard.html',
                           history=history,
                           preload=TMP_history,
                           devices=src.getDevices())


@app.route('/delete/<int:id>')
def delete(id):
    item2del = History.query.get_or_404(id)
    try:
        db.session.delete(item2del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ooops ... 502 BAD GATEWAY'
@app.route('/load/<int:id>')
def load(id):
    item2load = History.query.get_or_404(id)
    history = History.query.order_by(History.date).all()
    return render_template('dashboard.html',
                           history=history,
                           preload=item2load,
                           devices=src.getDevices())

@app.route('/slm', methods=['POST'])
def slm():
    global TMP_history
    global TMP_values
    TMP_history.dest = str(request.form['slm'])
    print(TMP_history)
    try:
        if(TMP_history.status == UNSAVED):
            db.session.add(TMP_history)
            for item in TMP_values:
                db.session.add(item)
            db.session.commit()
        history = History.query.order_by(History.date).all()
        return render_template('dashboard.html',
                           history=history,
                           preload=TMP_history,
                           devices=src.getDevices())
    except:
            return 'Ooops ... 502 BAD GATEWAY'


@app.route('/refreshSLM')
def refreshSLM():
    return redirect('/')


@app.route('/ack', methods=['GET'])
def acknowledge():
    return {'msg': 'Server OK'}


# ----------- MAIN
if __name__ == "__main__":
    src.welcome()
    # print(os.system(src.TUNNEL_CMD))
    # input('#### PRESS ANY KEY ####')
    app.run()
    # try:
    # except Exception as ex:
    #     print('\t >> ERR: ' + ex)
