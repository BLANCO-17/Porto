from genericpath import isfile
import os, sys, json, pickle

from flask.json import jsonify

_PATH = os.getcwd()

def pre_setup():
    try:
        os.mkdir("./data")
    except Exception as e:
        print(e)

def checkTrade(itemname, user):    
    return (os.path.isfile("..\\data\\"+user+"\\Trades\\"+itemname+".dat"))
        
def LoadObject(item, user):
    return pickle.load(open("..\data\\"+user+"\\Trades\\"+item+".dat", "rb"))

def getItems(username):
        try:
            file = open("..\\data\\"+username+"\\log.dat", "r")
            data = file.read()
            l = json.loads(data)
            return l
        except:
            print("error with loading items")
            return {"output": "error"}  

class User:

    def __init__(self, username, pin):
        self.name = username
        self.passcode = str(pin)
        self.items = []

    def createUser(self):
        try:
            os.mkdir("..\\data\\"+self.name)
            os.mkdir("..\\data\\"+self.name+"\\Trades")
            file = open("..\\data\\"+self.name+"\\log.dat", "w+")
            file.close()
            print("User created.")
        except Exception as e:
            print(e)
              

class TradeChain:
    cost = None
    shares = None
    next = None
    prev = None

class Trades:
    
    def __init__(self, name, cur):
        self.name = name
        self.cur = cur
        self.head = TradeChain()
        self.current = self.head

    def addTrade(self, cost, shares):
        temp = TradeChain()
        temp.cost = cost
        temp.shares = shares
        
        temp.prev = self.current
        self.current.next = temp
        self.current = self.current.next

    def saveObject(self, user):

        file = open("..\\data\\"+str(user)+"\\Trades\\"+self.name+".dat", "wb")
        pickle.dump(self, file)
        file.close()    
    
    def getTrades(self):
        temp = self.head.next        
        trades={}
        i=0
        while temp != None:
            # print(temp.cost)
            i+=1
            trades["trade "+str(i)] = {"cost":str(temp.cost), "shares":str(temp.shares)}
            temp = temp.next
        
        return trades
    
    def printdata(self):
        temp = self.head.next
        while temp != None:
            print(temp.shares, temp.cost)
            temp = temp.next

    def getTotalDetails(self):
        shares=0
        cost=0
        temp = self.head.next
        while temp != None:
            # print(temp.cost)
            cost += float(temp.cost) * float(temp.shares)
            shares += float(temp.shares)
            temp = temp.next
        return shares, cost
        
    def getCur(self):
        return self.cur


# tr = Trades("BTC", "INR")
# tr.addTrade(430, 15)
# tr.addTrade(460, 20)

# us = User("user2", 1234)
# us.createUser()
# print(os.path.exists("..\\data\\test"))
# tr.saveObject("test")
# tr.printdata()
# tr = pickle.load(open("..\data\\test\\Trades\\BTC.dat", "rb"))
# tr.printdata()

# file = open("..\\data\\test\\log.dat", "w+")
# file.truncate(0)
# data = "{\"user\":\"bossman\",\"items\":\"BTC, ETH\"}"
# file.write(data)
# file.close()
# file = open("..\\data\\test\\log.dat", "r")
# all_data = file.read()
# n = json.loads(all_data)
# lista = n['items'].split(',')
# print(lista)
# file.close()

