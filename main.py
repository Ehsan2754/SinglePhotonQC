import cmd
import time
import os
import json
if __name__ == "__main__":
    cmd.welcome()
    try:
        with open(cmd.USERINFO,'r') as userinfo:
            file = json.load(userinfo)
    except FileNotFoundError :
        
    
    