from flask import Flask, request, jsonify
from initialization import User, Trades, checkTrade, LoadObject
import pickle, json

app = Flask(__name__)

def addItem(user, item):
    file = open("..\\data\\"+str(user)+"\\log.dat", "r")
    all_data = file.read()
    file.close()
    obj = json.loads(all_data)
    list_obj = obj['items'].split(',')

    if str(item) not in list_obj:
        list_obj.append(item)
    

    # data = b"{\"user\":\""+user+"\",\"items\":\""+list_obj+"\"}"
    file = open("..\\data\\"+user+"\\log.dat", "w+")
    file.truncate(0)
    obj['items'] = list_obj    
    file.write(json.dumps(obj))    
    file.close()
    
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
    user = data.get("user")

    if checkTrade(name, user):
        obj = LoadObject(name, user)
        obj.addTrade(cost, share)
        obj.saveObject(user)
        addItem(user, name)
        # obj.printdata()
    else:
        tr = Trades(name, cur)
        tr.addTrade(cost, share)
        tr.saveObject(user)

    out = {"output": data}
    return out

@app.route("/getTrade")
def getTrade():
    data = request.args
    item = data.get("item")
    user = data.get("user")      
    # print("new Req")  
    tr = pickle.load(open("..\data\\"+user+"\\Trades\\"+item+".dat", "rb"))
    td = tr.getTrades()    
    # trades = jsonify(td)
    # print(trades)
        
    return jsonify(td)

@app.route("/getItems")
def getItems():

    user = request.args.get("user")
    pass

if __name__ == "__main__":    
    app.run()

# addItem("test", "MATIC")