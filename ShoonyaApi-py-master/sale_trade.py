import time
import pandas as pd
import csv
import order1
from dom import DomClass,PositionDOM,SupportDOM,OrderDOM,CEPENamingRule
import datetime
from file_manager import MyConfigReader
import os
import sound_data


os.system(f'title Sale_Order_Placing')
def countdown():
    lstPosition=[]
    lstSale_Data=[]
    curr_date=datetime.datetime.now()
    v_counter=0
    file_var=MyConfigReader()     
    #  myList=obj1.getOrderList() # order type=sale
    #  print("Open Orders:\n")
    #  if myList is not None:
    #   for item in myList:
    #   #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
    #    if  item['status']!='CANCELED' and item['status']!='REJECTED' and item['status']!='COMPLETE':        
    #       lstOrder.append(item['tsym'])

    while v_counter<3:
        #Actual function is here        
        buy_path=file_var.option_file
        lstBuy_Order=read_buy_options(buy_path) #read Order CSV File
        lstBuy_Stock=read_buy_stocks(file_var.stock_file) #read Order CSV File
         #Get Positions
        lstPosition=get_positions()
         #sell order check position
        if len(lstPosition)>0:
          #place sale order
          for item in lstPosition:
            balance_qty=float(item.netqty)
            if balance_qty>0:
                for csv_item in lstBuy_Order: #check target price from csv
                 if csv_item.name==item.name: #means option buy is in position
                  if item.name not in lstSale_Data: #sale list   
                    if checkSaleOrder(item.name)==True:          
                        lstSale_Data.append(item.name)                    
                        obj_sale= order1.MyClass()
                        activeOrderId=obj_sale.place_NSE_Option_Order_Sell(item.name,csv_item.target,item.daybuyqty)
                        sound_data.play_sound(item.name+" Sale Order done!")
                #stocks order
                if lstBuy_Stock is not None:
                 for csv_item_stock in lstBuy_Stock: #check target price from csv
                  if csv_item_stock.name==item.name: #means option buy has been done
                   if item.name not in lstSale_Data: #sale list  
                    if checkSaleOrder(item.name)==False:           
                        lstSale_Data.append(item.name)
                        obj_sale= order1.MyClass()
                        activeOrderId=obj_sale.place_NSE_Order_Sell(item.name,csv_item_stock.target,item.daybuyqty)
                        sound_data.play_sound(item.name+" Sale Order done!")
                           
                            
        
        #wait for 10 second
        time.sleep(10)
        curr_time=curr_date.time()
        print(curr_time)
    print("Place Enter to Close!")


  

def checkSaleOrder(stockName):  
    var_bln=True
    try:
        obj1=order1.MyClass()
        myList=obj1.getOrderList() # order type=sale
        if myList is not None:
            for item in myList:
        #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
                if  item['status']=='OPEN' and item['trantype']=='S' and stockName== item['tsym']:
                    print(item) #norenordno
                    var_bln=False
                    break  

    except Exception as e:
       print(f"An error occurred: {e}")
            
    return var_bln


def checkPosition(stockName,lstPosition):  
    var_found=False
    for item1 in lstPosition:
      if item1['daysellqty']=='0' and item1['tsym']==stockName:
            var_found=True
            break
      
    return var_found


def get_positions():
    lstPosition_temp=[]
    try:
        obj1= order1.MyClass()
        myPosition=obj1.getPositions()
        print(myPosition)
        print("Open Position:\n")
        if myPosition is not None:
          for item1 in myPosition:
            varOP= PositionDOM()
            varOP.name=item1['tsym']
            varOP.exch=item1['exch']
            varOP.qty=item1['daybuyqty']
            varOP.daybuyqty=item1['daybuyqty']
            varOP.daysellqty=item1['daysellqty']
            varOP.daybuyavgprc=item1['daybuyavgprc']
            varOP.daysellavgprc=item1['daysellavgprc']
            varOP.ltp=item1['lp']
            varOP.netqty=item1['netqty']
            varOP.profit_amt=item1['rpnl']
            print(varOP.name)
            lstPosition_temp.append(varOP)
    except Exception as e:
        print(f"An error occurred: {e}")

    return lstPosition_temp

def read_buy_options(path):   
    xlistStock =[]    
    if os.path.exists(path): 
     with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
            xObj = DomClass()
            xObj.expiry_dt = row[0]
            xObj.cepe_type = row[1]
            xObj.strike_rate = row[2]     
            xObj.buy = float(row[3])
            xObj.target = float(row[4])       
            xObj.stoploss = row[5]
            xObj.quantity=row[6]
            xObj.name=CEPENamingRule.get_cepe_admin_shoonya(xObj.expiry_dt,xObj.strike_rate,xObj.cepe_type)         
            xlistStock.append(xObj)
            print(f"Stock: {xObj.name}, Buy: {xObj.buy}, Target: {xObj.target}, StopLoss: {xObj.stoploss}")         
    return xlistStock

def read_buy_stocks(path):   
    xlistStock =[]     
    if os.path.exists(path):
     with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
            xObj = DomClass()
            xObj.name = row[0]
            xObj.quantity=row[1] 
            xObj.buy = float(row[2])
            xObj.target = float(row[3])       
            xObj.stoploss = row[4]
            xObj.averaging_count= row[5]            
            xlistStock.append(xObj)         
            print(f"Stock: {xObj.name}, Buy: {xObj.buy}, Target: {xObj.target}, StopLoss: {xObj.stoploss}")
        return xlistStock

    
countdown()
