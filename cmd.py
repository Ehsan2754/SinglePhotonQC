import time
import os

USERINFO = "USERINFO.json"
user = {
    "status" : None,
    "targetIP" : None,
    "targetPort" : None
}

def welcome():
    os.system("cls")
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('$$$ PLUTO 2.0 FTP SOFTWARE $$$')
    print('$$$      CLIENT/SERVER     $$$')
    print('$$$ AUTHOR: Ehsan Shaghaei $$$')
    print('$$$   Ehsan2754@yahoo.com  $$$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    time.sleep(2)

def getUserInfo_screen():
    
