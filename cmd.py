import time,os,pip._vendor.requests as requests
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

