from api_helper import ShoonyaApiPy
import datetime
import logging
import time
import yaml
import pandas as pd
from connection import MyAPIConnection
 
logging.basicConfig(level=logging.DEBUG)

#flag to tell us if the websocket is open
socket_opened = False

#application callbacks
def event_handler_order_update(message):
    print("order event: " + str(message))


def event_handler_quote_update(message):
    #e   Exchange
    #tk  Token
    #lp  LTP
    #pc  Percentage change
    #v   volume
    #o   Open price
    #h   High price
    #l   Low price
    #c   Close price
    #ap  Average trade price

    print("quote event: " + str(message))
    

def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')
    #api.subscribe_orders()
    #api.subscribe(['NSE|22', 'BSE|522032'])

#end of callbacks

def place_order_option(symb,price,qty):    
    con_obj=MyAPIConnection()
    api = ShoonyaApiPy()
    api=con_obj.get_api_connection()
    ret = api.place_order(buy_or_sell='B', product_type='M',
                        exchange='NFO', tradingsymbol=symb, 
                        quantity=qty, discloseqty=0,price_type='LMT', trigger_price=None,
                        retention='DAY', price=price, remarks='my_order_001')
    print(ret)

 
        
def place_sell_order_option(symb,price,qty):    
    con_obj=MyAPIConnection()
    api = ShoonyaApiPy()
    api=con_obj.get_api_connection()
    ret = api.place_order(buy_or_sell='S', product_type='M',
                        exchange='NFO', tradingsymbol=symb, 
                        quantity=qty, discloseqty=0,price_type='LMT', trigger_price=None,
                        retention='DAY', price=price, remarks='my_order_001')
    print(ret)

 
            
        


    