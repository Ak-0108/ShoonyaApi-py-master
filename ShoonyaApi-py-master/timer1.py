import time
import pandas as pd
import csv
import order1
from dom import DomClass,PositionDOM,SupportDOM
import datetime
from file_manager import MyConfigReader
from get_price_cls import PriceReaderClass
import order_live


objConfig=MyConfigReader()
root_folder=objConfig.root_folder +"\\"
folder_shoonya=objConfig.root_folder +"\\"+"shoonya\\"
# lst_files.append("support-high.csv")
# lst_files.append("buy-range.csv")
# lst_files.append("sell-range.csv")
# above three is used by stock-auto\stockcode\nifty-support-high
# lst_files.append("trade-fno.csv")
# lst_files.append("trade-stock.csv")
support_file_auto=root_folder+"support-auto.csv" #entered by nifty-support-high scheduler
support_file_manual=folder_shoonya+"support.csv" # have CE or PE Prcie entered by admin base entry
manual_option_file= root_folder+ "trade-fno.csv" #created based on admin setting
stocks_file= root_folder + 'trade-stock.csv'   #created based on admin setting

def countdown():
     lstPosition=[]
     lstOrder=[]
     lstSale_Data=[]
     
     lstData=[]
     objOld=DomClass()
     obj1= order1.MyClass()
     objPriceReader=PriceReaderClass()
     xlistStock=readcsv(manual_option_file)
     
     #cancel order
     #cancel_open_order(obj1)
     #end of cancel order

     myList=obj1.getOrderList()
     print("Open Orders:\n")
     if myList is not None:
      for item in myList:
      #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
       if  item['status']!='CANCELED' and item['status']!='REJECTED':
          print(item) #norenordno
          lstOrder.append(item['norenordno'])
          #orderNo=item['norenordno']
          #obj1.cancel_Order(orderNo)
    
     #Get Positions
     lstPosition=get_positions(obj1=obj1)

     #activeOrderId=obj1.place_NSE_Option_Order_Sell('NIFTY26JUN25P24800',70,75)
    
     while v_counter<3:
        #Actual function is here
         supportObj=readcsv_list(support_file_manual)
         for objY in supportObj:
          #if check_add_order(objY.name,objY.buy,lstOrder)==False:
           if check_add_order(objY.name,objY.buy,lstData)==False:
             if objY.is_option=='Y':               
              #current_price=objPriceReader.read_ce_pe_rate(objY.name)
              #if current_price>=objY.buy:
                 buy_p=objPriceReader.read_ce_pe_rate(objY.name)
                 activeOrderId=order_live.place_order_option(objY.name,buy_p-1,objY.quantity)                  
                 lstData.append(objY)
             else:
               #current_price=objPriceReader.read_stock_rate(objY.name)
               #if current_price>=objY.buy:
                 activeOrderId=obj1.place_NSE_Order(objY.name,objY.buy,objY.quantity) 
                 #activeOrderId=obj1.place_NSE_Option_Market_Order(objY.name,objY.quantity) 
                 lstData.append(objY)
            #END OF CHECK ORDER
         
         #CE or PE to be entered by admin
         manualOption=readcsv_list(manual_option_file)
         for objY2 in manualOption:
          #if check_add_order(objY.name,objY.buy,lstOrder)==False:
           if check_add_order(objY2.name,objY2.buy,lstData)==False:         
              #current_price=objPriceReader.read_ce_pe_rate(objY2.name)
              #if current_price>=objY2.buy:
                 activeOrderId=obj1.place_NSE_Option_Order(objY2.name,objY2.buy,objY2.quantity) 
                 lstData.append(objY2)

            #END OF CHECK ORDER


        #Trade Stock Only
         xlistStock=readcsv(stocks_file)
         for stockObj in xlistStock:
          if stockObj.name!='' and stockObj.buy!="0":
           if check_add_order(stockObj.name,stockObj.buy,lstData)==False:
            print("New Order Placed")
            activeOrderId=obj1.place_NSE_Order(stockObj.name,stockObj.buy,stockObj.quantity)         
            lstData.append(stockObj)
         # elif(objOld.buy!=stockObj.buy):
         #   objOld.buy=stockObj.buy
         #   print('buy price is modified at {objY.buy}')
         #   obj1.modify_order(activeOrderId,objY.buy)

         
         #Get Positions
         lstPosition=get_positions(obj1=obj1)
         #sell order check position
         if len(lstPosition)>0:
          #place sale order
          for item_buy in lstData: #buy list
            if item_buy.name not in lstSale_Data: #sale list
             if checkBuyPosition(item_buy.name,lstPosition)==True: #check if buy order executed THEN ONLY SALE
                lstSale_Data.append(objY.name)
                if item_buy.is_option=='Y':
                 activeOrderId=obj1.place_NSE_Option_Order_Sell(stockObj.name,stockObj.target,stockObj.quantity)
                else:
                 activeOrderId=obj1.place_NSE_Order_Sell(stockObj.name,stockObj.target,stockObj.quantity)
               
         
        
        #wait for 10 second
         time.sleep(10)
         curr_time=curr_date.time()
         print(curr_time)
     print("Place Enter to Close!")


  
#order to be place only once
def check_add_order(stockName,buyPrice,myList):
   found = False
   for item in myList:
       if item.name == stockName and item.buy==buyPrice:
           found = True
           break
   return found

def checkBuyPosition(stockName,lstPosition):  
    var_found=False
    for item1 in lstPosition:
      if item1['daysellqty']=='0' and item1['tsym']==stockName:
            var_found=True
            break
      
    return var_found


def checkPosition(stockName,lstPosition):  
    var_found=False
    for item1 in lstPosition:
      if item1['daysellqty']=='0' and item1['tsym']==stockName:
            var_found=True
            break
      
    return var_found

#used to cancel order
def cancel_open_order(obj1):  
    myListCancel=obj1.getOrderList()
    if myListCancel is not None:
      for citem in myListCancel:
         if citem['status']=='OPEN':
          orderno=citem['norenordno']  
          obj1.cancel_Order(orderno)

def get_positions(obj1):
        myPosition=obj1.getPositions()
        lstPosition_temp=[]
        print("Open Position:\n")
        if myPosition is not None:
          for item1 in myPosition:
            varOP= PositionDOM()
            varOP.name=item1['tsym']
            varOP.exch=item1['exch']
            varOP.qty=item1['ls']
            varOP.daybuyqty=item1['daybuyqty']
            varOP.daysellqty=item1['daysellqty']
            varOP.daybuyavgprc=item1['daybuyavgprc']
            varOP.daysellavgprc=item1['daysellavgprc']
            varOP.ltp=item1['lp']
            varOP.netqty=item1['netqty']
            print(varOP.name)
            lstPosition_temp.append(varOP)
        return lstPosition_temp

def readcsv(path):
    xlistStock =[]     
    with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
            if len(row)==0:
               break
            xObj = DomClass()
            xObj.name = row[0]
            xObj.buy = float(row[1])
            xObj.target = float(row[2])       
            xObj.stoploss = row[3]
            xObj.quantity=row[4]
            xlistStock.append(xObj)
            print(f"Stock: {xObj.name}, Buy: {xObj.buy}, Target: {xObj.target}, StopLoss: {xObj.stoploss}")
            
    return xlistStock

def readcsv_list(path):
    xlist =[] 
    with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
         if len(row)==0:
            break
         xObj=DomClass()
         xObj.name = row[0]
         xObj.buy = float(row[1])
         xObj.target =float(row[2])         
         xObj.stoploss = row[3]
         xObj.quantity=row[4]
         xObj.is_option=row[5]
         xlist.append(xObj)
    return xlist

def readcsv_support(path):
    xlist =[] 
    with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
         if len(row)==0:
            break
         xObj=SupportDOM()
         xObj.support = float(row[0])
         xObj.resistance =float(row[1])         
        
         xlist.append(xObj)
    return xlist

curr_date=datetime.datetime.now()
v_counter=0    
countdown()
