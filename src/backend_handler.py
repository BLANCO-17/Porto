from flask import Flask, request, jsonify
from initialization import User, Trades, checkTrade, LoadObject, getItems
import pickle, json, sys, time, atexit, os
from threading import Thread

app = Flask(__name__)

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
    time.sleep(1)
    os._exit(0)
    # raise RuntimeError("shtting down")
    

@app.route("/")
def home():
    return "homepage"

@app.route("/createTrade")
def createTrade():
    data = request.args
    name = data.get("name")
    cur = data.get("CUR")
    cost = data.get("cost")
    share = data.get("shares")
    # user = data.get("user")

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

    user = str(request.args.get('user'))    
    itemlist = getItems("user")['items']
    # print(itemlist)
    # for x in itemlist:
    #     print(cleanString(x))
    # out = [x.strip() for x in itemlist.split(',')]
    # print(out['items'].split(',')[0])
    
    return {"items": itemlist}

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
    app.run()
