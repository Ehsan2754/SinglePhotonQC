

from flask import  render_template, url_for, request, redirect,session
from flask_ngrok import run_with_ngrok
from app import app
from app.models.dataModel import Superposition ,LG_Values,Devices
from app.holoeye import detect_heds_module_path, slmdisplaysdk
from app import src

# ----------- Constants
DEFAULT_IMG = 'img/default.jpg'
TMP_IMG = 'img/tmp.bmp'
UNSAVED = False
SAVED = True
INIT_form = Superposition()
TMP_SP = Superposition()
TMP_values = []


# ----------- REST-FUL API SERVICE
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return 'post'
    else:
        return render_template('dashboard/dashboard.html',
                               user = 'Ethan',
                               records=[],
                               default=Superposition(gussian_waist=0),
                               devices=src.getDevices())


@app.route('/plot', methods=['POST','GET'])
def plot():
    if request.method == 'POST':
        session['form']=request.form
        session['user']='Ehsan'
        session['records']=[]
        session['devices']=src.getDevices()
        default = Superposition(**src.normalizeValues(request.form))
        return render_template('dashboard/dashboard.html',
            **session,
            default=default)


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
    try:

        ErrorCode = slmdisplaysdk.SLMDisplay.ErrorCode
        ShowFlags = slmdisplaysdk.SLMDisplay.ShowFlags
        slm = slmdisplaysdk.SLMDisplay()
        error = slm.open()
        form = src.normalizeValues(session['form'])
        form['destination']= Devices(name=request.form['slm'])
        print(form['destination'])
        form["width"] =  slm.width_px #or 1920
        form["height"] = slm.height_px #or 1080
        default = Superposition(**form)
        data=default.get_Superposition()
        print("dataWidth = " + str(slm.width_px))
        print("dataHeight = " + str(slm.height_px))
        error = slm.showData(data)
        return render_template('dashboard/dashboard.html',
            **session,
            default=default)
    except Exception as ex:
            return 'Ooops ... 502 BAD GATEWAY'+str(ex)


@app.route('/refreshSLM')
def refreshSLM():
    return redirect('/')


@app.route('/ack', methods=['GET'])
def acknowledge():
    return {'msg': 'Server OK'}
