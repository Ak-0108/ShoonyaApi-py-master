import time
import pandas as pd
import csv
import sound_data
from dom import DomClass,PositionDOM,PricekDOM
import datetime
from mcx_reader import PriceReaderClass 


def countdown():
     lstItem=[]
     
     objOld=DomClass()
     #obj1= order1.MyClass()
     #myPosition=obj1.getPositions()
     activeOrderId=''
      
     readerObj=PriceReaderClass()
     # stockname='NATGASMINI24JUL25C320'
     # price=readerObj.read_stock_price_MCX(stockname)
     # print(price['lp'])
     #priceData=readerObj.read_stock_price_MCX('CRUDEOILM17JUL25C57')
     priceData=readerObj.read_stock_price_MCX('NATGASMINI24JUL25C320')
     #print(priceData)
     #token=priceData['token']
     ltp=priceData['lp']
     print(ltp)
     sound_data.play_sound(str(ltp))
#      objchart=readerObj.read_mcx_chart('CRUDEOILM21JUL25',token)
#      print(objchart)


     # priceObj=PricekDOM()
     # if priceData is not None:
     #  priceObj.rate=priceData['lp']
     #  priceObj.open=priceData['o']
     #  priceObj.close=priceData['c']
     #  priceObj.high=priceData['h']
     #  priceObj.low=priceData['l']
     #  priceObj.average=priceData['ap']
     #  print( priceObj.rate)
   
     # lotSize=priceData['ls']

     # if float(priceObj.rate)> float(priceObj.low):
     #    print(priceObj.rate)
        #activeOrderId=obj1.place_MCX_Order(stockname,7, lotSize)  

curr_date=datetime.datetime.now()
v_counter=0  
while v_counter==0:  
 countdown()
 time.sleep(10)
