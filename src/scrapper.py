#AUTHOR - BLANCO
#WEBSCRAPPER FOR EXTRACTING CRYPTO PRICES FROM COINMARKETCAP

#Refer to the getName() function to see default supported coins, feel free to add coins of your choice.

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

class priceExtractor:
    
    def __init__(self):    

        self.option = webdriver.ChromeOptions()
        self.option.add_argument("disable-gpu")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-sh-usage') 
        self.option.add_experimental_option('excludeSwitches', ['enable-logging']) #comment this code if you want the webdriver logs in console
        chromedriver_autoinstaller.install()

        # path=Service("C:\Program Files (x86)\ChromeDriver\chromedriver.exe")        
        self.driver = webdriver.Chrome(options=self.option)
            
    def getName(self, abv):
        
        # NAME VALUE pairs based on coinmarketcap item's url
        # Add available crypto names and abbreviations of your choice
        # The value of the abbreviation should be one that is being used in the url of coinmarketcap
        #i,e for btc valid url is https://coinmarketcap.com/currencies/bitcoin/ - so we added bitcoin as value for key btc below
        
        name_dict = {}
        name_dict['btc'] = 'bitcoin'
        name_dict['eth'] = 'ethereum'
        name_dict['ada'] = 'cardano'
        name_dict['xrp'] = 'xrp'
        name_dict['xlm'] = 'stellar'
        name_dict['luna'] = 'terra-luna'
        name_dict['bnb'] = 'binance-coin'
        name_dict['sol'] = 'solana'
        name_dict['dot'] = 'polkadot-new'
        name_dict['avax'] = 'avalanche'
        name_dict['matic'] = 'polygon'
        name_dict['link'] = 'chainlink'
        name_dict['mana'] = 'decentraland'
        name_dict['mina'] = 'mina'
        name_dict['vet'] = 'vechain'
        name_dict['atom'] = 'cosmos'
        name_dict['sand'] = 'the-sandbox'
        name_dict['hbar'] = 'hedera'
        name_dict['gala'] = 'gala'
        name_dict['eos'] = 'eos'
        name_dict['reef'] = 'reef'
        name_dict['ltc'] = 'litecoin'
        name_dict['uni'] = 'uniswap'
        name_dict['algo'] = 'algorand'
        name_dict['trx'] = 'tron'
        name_dict['fil'] = 'filecoin'
        name_dict['gala'] = 'gala'

        return name_dict.get(abv)
            
    def getPrice(self, coinname):

        abv = self.getName(coinname)
        
        if(abv != None):
                    
            self.driver.get('https://coinmarketcap.com/currencies/'+abv+'/') # Getting page HTML through request
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
            data = self.soup.find("div", {"class": "priceValue"}) # Selecting priceValue Class object
            
            try:
                price = (data.string).replace("$", "")
                temp = price.replace(",", "")
                price = temp
            except:
                pass
                
            # print(price)
            return float(price)
        else:
            print("[ERROR] - Item not yet supported. Take a look at the 'getName' function of this class.")
            return 0
    
    def closeDriver(self):
        #always call this function before closing your main script, responsible for flushing the webdriver.exe        
        self.driver.quit()
    
    def __del__(self):
        try:
            self.closeDriver()
        except:
            pass
    

#USAGE
# pe = priceExtractor()
# print(pe.getPrice('btc')) 

#------------------
# pe.closeDriver() # -> important to call whenever closing application / script.