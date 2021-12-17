from flask import Flask, request, jsonify
from initialization import User, Trades, checkTrade, LoadObject, getItems
from threading import Thread
from priceExtQ import Queue
from forex_python.converter import CurrencyRates
import pickle, json, sys, time, atexit, os

app = Flask(__name__)
priceExtractors = {}
myQueue = Queue()

_LOGGED = False
_FIATS = {}
         

def initialize():
    global _FIATS
    
    c = CurrencyRates()    
        
    _FIATS['INR'] = c.get_rate('USD', 'INR')
    _FIATS['EUR'] = c.get_rate('USD', 'EUR')
    _FIATS['USDT'] = 1#c.get_rate('USD', 'USD')    
    _FIATS['USD'] = 1#c.get_rate('USD', 'USD')    

def addItem(user, item):
    file = open("..\\data\\user\\log.dat", "r")
    all_data = file.read()
    file.close()
    obj = json.loads(all_data)
    list_obj = obj['items']

    # print(list_obj)
    # print(item)
    if str(item) not in list_obj:
        list_obj.append(item)
    
    # data = b"{\"user\":\""+user+"\",\"items\":\""+list_obj+"\"}"
    file = open("..\\data\\"+user+"\\log.dat", "w+")
    file.truncate(0)
    obj['items'] = list_obj    
    file.write(json.dumps(obj))    
    file.close()
    
def closeApp():

    myQueue.closeQ()
    
    time.sleep(1)
    os._exit(0)
    # raise RuntimeError("shtting down")
    
def getPriceFunc(coin):   
    price = priceExtractors[coin].getPrice(coin)
    print("output:",coin, price)
    return {"price":price}


initialize()

@app.route("/")
def home():
    return {"output": "started"}

@app.route("/createTrade")
def createTrade():    
    
    data = request.args
    name = data.get("name")
    cur = data.get("CUR")
    cost = data.get("cost")
    share = data.get("shares")

    if not checkTrade(name, user="user"):
        tr = Trades(name, cur)
        tr.addTrade(cost, share)        
        tr.saveObject("user")
        addItem("user", name)
        # obj.printdata()
    else:
        obj = LoadObject(name, "user")
        obj.addTrade(cost, share)
        obj.saveObject("user")

    out = {"output": data}
    return out

@app.route("/getTrade")
def getTrade():
    data = request.args
    item = data.get("item")    
    # user = data.get("user")
    # print("new Req")
    tr = pickle.load(open("..\data\\user\\Trades\\"+item+".dat", "rb"))
    td = tr.getTrades()
    # trades = jsonify(td)
    # print(trades)
        
    return jsonify(td)

@app.route('/getDetails')
def getTotalDets():
    data = request.args
    item = data.get("item")
    tr = pickle.load(open("..\data\\user\\Trades\\"+item+".dat", "rb"))
    shares, cost = tr.getTotalDetails()
    
    return {"shares": shares, "cost": cost}
    
@app.route("/getUserItems")
def getUserItems():
    
    global _LOGGED
    
    try:        
        user = str(request.args.get('user'))    
        itemlist = getItems("user")['items']
        
        # if(not _LOGGED):
        #     i=0
        #     for x in itemlist:
        #         priceExtractors[str(x).lower()] = priceExtractor()
            
        #     _LOGGED = True        
        
        # print(priceExtractors)
        return {"items": itemlist}
    except:
        return {"error" : "invalid user data request"}

    # print(itemlist)
    # for x in itemlist:
    #     print(cleanString(x))
    # out = [x.strip() for x in itemlist.split(',')]
    # print(out['items'].split(',')[0])

@app.route('/getPrice')
def getPrice():
    global priceExtractors
    
    data = request.args
    coin = data.get('item')
    cur = data.get('cur')
    # price = priceExtractors[coin].getPrice(coin)
    myQueue.sendToQueue(coin)

    if not myQueue.isRunning():
        myQueue.callQueue()
    
    price = None
    
    while True:
        price = myQueue.getPrice(coin)
        
        if price != None:
            break
        else:
            time.sleep(1)
        
    price = round((_FIATS[cur] * price), 2)                                                                                                                                                                 
        
    # print(price, coin)
    return {"price": price}
    
@app.route('/getItemCur')
def getCur():
    item = request.args.get('item')
    
    tr = pickle.load(open("..\data\\user\\Trades\\"+item+".dat", "rb"))
    cur = tr.getCur()
    
    return{"cur":cur}

@app.route('/systemcmds')
def systemCMD():
    cmd = request.args.get('cmd')
    if(cmd == "quit"):        
        print("closing application...")
        t = Thread(target=closeApp)
        t.setDaemon(False)
        t.start()
        return {"output": "closing App - executed"}
        

if __name__ == "__main__":
    
    try:
        user = User("user", "1234")
        user.createUser()
    except:
        pass       
    
    app.run()
