from scrapper import priceExtractor
from threading import Thread
from time import sleep
class Queue:
    
    def __init__(self) -> None:
        self.pe = priceExtractor()
        self.requests = []
        self.output = {}
        self.cmd = ""
        self._RUNNING = False
        print("Queue Initiated.")
        
        
    
    def sendToQueue(self, coin):        
        self.requests.append(coin)
        # print(len(self.requests))
        

    def getPrice(self, coin):
        # print(self.output[coin])
        try:
            return self.output[coin]
        except:
            return None

    def startQueue(self):
        
        while True:    
            
            if(len(self.requests)>0):
                item = self.requests.pop(0)
                tempPrice = self.pe.getPrice(item)
                self.output[item] = tempPrice
            else:
                self._RUNNING = False
                break
                # print("waiting")
            
    def callQueue(self):
        self._RUNNING = True
        self.t = Thread(target=self.startQueue)
        self.t.start()
    
    def isRunning(self):
        return self._RUNNING
        
    
    def closeQ(self):
        self.pe.closeDriver()
        

# q = Queue()
# q.sendToQueue('btc')

# while True:
#     out = q.getPrice('btc')
#     if out == None:
#         sleep(1)
#     else:
#         print(out)
#         break

# q.closeQ()