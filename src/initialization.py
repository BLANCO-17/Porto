import os, sys

_PATH = os.getcwd()

def pre_setup():
    try:
        os.mkdir("./data")
    except Exception as e:
        print(e)

    
class User:

    def __init__(self, username, pin):
        self.name = username
        self.passcode = str(pin)

    def createUser(self):
        try:
            os.mkdir(".\\data\\"+self.name)
        except Exception as e:
            print(e)

