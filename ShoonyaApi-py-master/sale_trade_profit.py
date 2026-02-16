import time
import pandas as pd
import csv
import order1
from dom import DomClass,PositionDOM,SupportDOM,OrderDOM,CEPENamingRule
import datetime
from file_manager import MyConfigReader
import os

os.system(f'title Sale_Order_Profit_Execute')
def countdown():
     lstPosition=[]
     lstSale_Data=[]
        
     file_var=MyConfigReader()     
    #  myList=obj1.getOrderList() # order type=sale
    #  print("Open Orders:\n")
    #  if myList is not None:
    #   for item in myList:
    #   #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
    #    if  item['status']!='CANCELED' and item['status']!='REJECTED' and item['status']!='COMPLETE':        
    #       lstOrder.append(item['tsym'])

     while v_counter<3:
         #Get Positions
        lstPosition=get_positions()
         #sell order check position
        if len(lstPosition)>0:
          #place sale order
          for item in lstPosition:
            balance_qty=float(item.netqty)
            if balance_qty>0:               
                  if item.name not in lstSale_Data: #sale list   
                    if checkSaleOrder(item.name)==False: 
                        if float(item.profit_amt)>150:
                            lstSale_Data.append(item.name)                    
                            obj_sale= order1.MyClass()
                            if item.exch=="NFO":
                                activeOrderId=obj_sale.place_NSE_Option_Order_Sell(item.name,item.ltp,item.netqty)
                            else:
                                activeOrderId=obj_sale.place_NSE_Order_Sell(item.name,item.ltp,item.netqty)
                    
        
        #wait for 10 second
        time.sleep(10)
        curr_time=curr_date.time()
        print(curr_time)
     print("Place Enter to Close!")


  

def checkSaleOrder(stockName):  
    var_bln=True
    obj1=order1.MyClass()
    myList=obj1.getOrderList() # order type=sale
    if myList is not None:
     for item in myList:
      #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
       if  item['status']=='OPEN' and item['trantype']=='S' and stockName== item['tsym']:
          print(item) #norenordno
          var_bln=False
          break       
    return var_bln


def checkPosition(stockName,lstPosition):  
    var_found=False
    for item1 in lstPosition:
      if item1['daysellqty']=='0' and item1['tsym']==stockName:
            var_found=True
            break
      
    return var_found


def get_positions():
        obj1= order1.MyClass()
        myPosition=obj1.getPositions()
        print(myPosition)
        lstPosition_temp=[]
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
        return lstPosition_temp


curr_date=datetime.datetime.now()
v_counter=0    
countdown()
