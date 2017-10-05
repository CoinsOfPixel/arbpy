#Python 2.7
#You must have to install twilio in your machine. pip install twilio
import json
import urllib2
import threading
from twilio.rest import Client

#Take the price from localbitcoins, bitstamp, usd price and Mercadobitcoin and foxbit
urlBTCUSD = 'https://www.bitstamp.net/api/ticker/'
urlBRL = 'http://api.fixer.io/latest?base=USD'
urlMercado = 'https://www.mercadobitcoin.net/api/BTC/ticker/'
urlFOXBIT = 'https://api.blinktrade.com/api/v1/BRL/ticker?crypto_currency=BTC'
urlLocalJson = 'https://localbitcoins.com/buy-bitcoins-online/USD/.json'

json_obj_BTCUSD = urllib2.urlopen(urlBTCUSD)
json_obj_BRL = urllib2.urlopen(urlBRL)
json_obj_Mercado = urllib2.urlopen(urlMercado)
json_obj_FOXBIT = urllib2.urlopen(urlFOXBIT)

btc = json.load(json_obj_BTCUSD)
brl = json.load(json_obj_BRL)
mb = json.load(json_obj_Mercado)
fb = json.load(json_obj_FOXBIT)

btcUSDPrice = float(btc['last'])
usdBRL = float(brl['rates']['BRL'])
mercadob = float(mb['ticker']['last'])
foxbit = float(fb['last'])

btcUSD2BRL = btcUSDPrice * usdBRL
btcBRLAverage = (mercadob + foxbit) / 2
difference = (abs(btcBRLAverage - btcUSD2BRL)) / btcBRLAverage * 100.0

#print('%.2f' %btcBRLAverage)
#print('%.2f' %btcUSD2BRL)
#print('%.2f' %difference)

urlUSDV = urlBRL
urlLCB = urlLocalJson
    
json_obj_USD = urllib2.urlopen(urlUSDV)
json_obj_LocalBtc = urllib2.urlopen(urlLCB)
    
usdPrice = json.load(json_obj_USD)
offer = json.load(json_obj_LocalBtc)
    
usd2BRL = float(usdPrice['rates']['BRL'])
    
position = 0

#Fees
#mbFee = 2% p 2.50
#fbFee = 2% p 9.00
#wuFee = 12.00
#lbFee = 1%
#amnt = 3500.00 #BRL
totalFee = 200
    
size = len(offer['data']['ad_list'][position]['data']['profile'])

def SMS(ID, profit):
    account_sid = "Your Twilio SID"
    auth_token = "Your Twilio auth token"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="Your mobile phone",
        from_="+Your twilio number",
        body="Take a look on the offer: %s - Possible profit: %.2f percent." %(str(ID), profit))
    print('SMS Sent')

def working():
    position = 0
    for i in range(size):
        position += 1
        seller = offer['data']['ad_list'][position]['data']['profile']['username']
        offerID = offer['data']['ad_list'][position]['data']['ad_id']
        price = float(offer['data']['ad_list'][position]['data']['temp_price_usd'])
        method = offer['data']['ad_list'][position]['data']['online_provider']
        if 'WU' in method:
            print('Seller: %s - Offer ID: %s  - by the price: %f - for the method: %s' %(seller, offerID, price, method))
            sellerBTC2BRL = usd2BRL * price                      
            print('Price in BRL: %.2f' %sellerBTC2BRL)
            diffSeller2BR = (abs(btcBRLAverage - sellerBTC2BRL - totalFee)) / btcBRLAverage * 100
            print('>>> Possible profit: %.2f percent' %(diffSeller2BR))
            if diffSeller2BR > 15: #You set here when send the allert. In my case if the profit > than 15%
                SMS(offerID, diffSeller2BR)
def contador():
    threading.Timer(20, contador).start()
    working()

contador()
