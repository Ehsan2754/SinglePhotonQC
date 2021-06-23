import time,os,pip._vendor.requests as requests
import base64
import numpy as np
import cv2
# --- CONSTANTS 
TGbot_TOKEN = 1
TUNNEL_CMD = 'ngrok.exe authtoken 1dQueKHOQWNNi5epQPMNhGfivjr_bhSPj14GGVekGETLre7j'
def createTunnel2tg(token):
    return requests.post(url='https://api.telegram.org/bot{token}/setWebhook')
def welcome():
    os.system("cls")
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('$$$ PLUTO 2.0 FTP SOFTWARE $$$')
    print('$$$      CLIENT/SERVER     $$$')
    print('$$$ AUTHOR: Ehsan Shaghaei $$$')
    print('$$$   Ehsan2754@yahoo.com  $$$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
def getDevices():
    return ['HOLOEYE-PLUTO2']
def getB64string(bin):
    return base64.b64encode(bin)
def getAxis(magnitute,shift):
    return np.linspace(-1*magnitute/2+shift,magnitute/2+shift-1,magnitute)
def lagurrelGussian(percision,shift):
    x = -percision/2
    output = np.array(percision*[0])
    for i in range(percision):
        output[i] = x+i+shift
    return output
def getSuperPosition():
    pass

from app.models.dataModel import LG_Values 
def normalizeValues(form):
    t = {key:form[key] for key in form}
    values = [ LG_Values(index=i,coefficient=float(t.pop('C'+str(i))),parameter=int(t.pop('LG'+str(i)))) for i in range(1,int(t['n_values'])+1)]
    t['values']=values
    return t


camera = cv2.VideoCapture(0)
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
