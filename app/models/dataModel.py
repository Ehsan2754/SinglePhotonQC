from app import db
from sqlalchemy_utils import IPAddressType


import time, os, json, base64
from io import BytesIO
from datetime import datetime

import numpy as np
from math import factorial
from scipy.special import assoc_laguerre as lg
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.figure import Figure


from app.holoeye import detect_heds_module_path, slmdisplaysdk



DEFAULT_IMG = 'img/default.jpg'
TMP_IMG = 'img/tmp.bmp'
UNSAVED = False
SAVED = True
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
    gussian_waist = db.Column(db.Integer, nullable=False)
    # --- Radial Index
    radial_index = db.Column(db.Integer, nullable=False)
    # --- Number of parameters for LG
    n_values = db.Column(db.Integer, nullable=False)
    # --- Values for LG parameters
    values = db.relationship('LG_Values', backref='Superposition')
    # --- Horizontal shift
    h_shift = db.Column(db.Integer, nullable=False)
    # --- Vertical Shift
    v_shift = db.Column(db.Integer, nullable=False)
    # --- Blaze Period
    blaze_period = db.Column(db.Float)
    # --- Scanning range
    scale = db.Column(db.Integer, nullable=False)
    # --- Image file
    image = db.Column(db.LargeBinary)
    # --- Creation date
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self,*args,**kwargs):
        self.height = int(kwargs['height']) if 'height' in kwargs else 1080
        self.width  = int(kwargs['width']) if 'width' in kwargs else 1920
        self.gussian_waist = int(kwargs['gussian_waist']) if 'gussian_waist' in kwargs else 100
        self.radial_index = int(kwargs['radial_index']) if 'radial_index' in kwargs else 0
        self.n_values = int(kwargs['n_values']) if 'n_values' in kwargs else 1
        self.values = kwargs['values'] if 'values' in kwargs else [LG_Values(index=0,coefficient=2,parameter=2)]
        self.h_shift = int(kwargs['h_shift']) if 'h_shift' in kwargs else 10
        self.v_shift = int(kwargs['v_shift']) if 'v_shift' in kwargs else 10
        self.blaze_period = float(kwargs['blaze_period']) if 'blaze_period' in kwargs else 5
        self.scale = float(kwargs['scale']) if 'scale' in kwargs else 0xff
        self.image = self.get_Superposition_image()
    def __repr__(self):
        return f'''
        <{id}>
        <{self.destination}>
        <{self.gussian_waist}>
        <{self.radial_index}>
        <{self.n_values}>
        <{self.values}>
        <{self.h_shift}>
        <{self.v_shift}>
        <{self.blaze_period}>
        <{self.scale}>
        <{self.date}>
        '''

    def get_LG_pairs(self,values=None):
        '''
        @input:  
        values=a list of Value 'obj'
        @returns a list of Value pairs
        '''
        values = self.values if not values else values
        buffer = {t.index:(t.parameter,t.coefficient) for t in values}
        buffer_s = {k: buffer[k] for k in sorted(buffer)}
        return [buffer_s[i] for i in buffer_s]

    def getAxis(self,magnitute,shift):
        '''
        @input: 
        magnitute=the length 
        shift=shifting #unit
        @returns
        a symmetric vector of axis with length if "magnitute" and "shift" units shifted
        '''
        return np.linspace(-1*magnitute/2+shift,magnitute/2+shift-1,magnitute)

    def car2polar(self,x,y):
        '''
        transforms Cartisian system into Polar system
        '''
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
        return self.N_PL(p,l)*np.power(np.sqrt(2)*rho2w,abs(l))*lg(2*np.power(rho2w,2),p,abs(l))*np.exp(-1*np.power(rho2w,2))*np.exp(complex(0,-1)*l*phi)

    def get_Superposition(self,width=None,height=None,h_shift=None,v_shift=None,w=None,p=None,values=None,bp=None,scale=None):
        
        width=self.width if not width else width
        height=self.height if not height else height
        h_shift=self.h_shift if not h_shift else h_shift
        v_shift=self.v_shift if not v_shift else v_shift
        w=self.gussian_waist if not w else w
        p=self.radial_index if not p else p
        values=self.get_LG_pairs()
        bp = self.blaze_period if not bp else bp
        scale = self.scale if not scale else scale
        x, y     = self.getAxis(width,h_shift),self.getAxis(height,v_shift)
        xv, yv   = np.meshgrid(x,y)
        rho, phi = self.car2polar(xv,yv)
        out  = 0
        for m,n in values:
            temp = n*self.lagurrelGussian(rho,phi,w,m,p)
            out += temp  
        amp   = np.absolute(out)
        amp=amp/np.amax(amp)
        phase = np.angle(out)  - np.pi*amp
        phase_mod = (phase+2*np.pi*xv/bp) % (2*np.pi)   
        result = amp*phase_mod
        scaled_result= result/result.max()*scale
        return scaled_result.astype(np.uint8) 
        
    
    def get_Superposition_image(self):
        out = self.get_Superposition()
        buf = BytesIO()
        plt.imsave(buf,out, cmap="gist_gray", vmin = 0,vmax=self.scale,format="png")
        return base64.b64encode(buf.getbuffer()).decode("ascii")

class LG_Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Superposition_id = db.Column(db.Integer, db.ForeignKey('Superposition.id'))
    index = db.Column(db.Integer, nullable=False)
    coefficient = db.Column(db.Float, nullable=False)
    parameter = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<i={},p={},c={}>'.format(self.index, self.parameter,
                                         self.coefficient)

class Devices(db.Model):
    __tablename__ = 'Devices'
    id = db.Column(db.Integer, primary_key=True)
    Superposition_id = db.Column(db.Integer, db.ForeignKey('Superposition.id'))
    name = db.Column(db.String(length=255))
    ip_addr = db.Column(IPAddressType)
    port = db.Column(db.Integer)
    # DeviceType_id = db.relationship('DeviceType', backref='Devices')
    def get_devices():
        pass
    def rcv_data():
        pass
    def send_Data():
        pass
