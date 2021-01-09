import time,os,json,threading as td,cmd
from cmd import welcome
from flask import  Flask,render_template, url_for, request, redirect
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
# ----------- BOT-ACTIVATION
# ----------- REST-FUL API SERVICE
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('dashboard.html')
@app.route('/ack',methods=['GET'])
def acknowledge():
    return {'msg':'Server OK'}



# ----------- MAIN
if __name__ == "__main__":
    welcome()
    print(os.system(cmd.TUNNEL_CMD))
    # input('#### PRESS ANY KEY ####')
    try:
        app.run(debug=True)
    except Exception as ex :
        print ('\t >> ERR: '+ ex)
    
