import time
import csv
from datetime import datetime
from dom import DomClass
import order1
import os

os.system(f'title Start_Stock_Trade')
def countdown():     
    order_count=0
    bln_order_placed=False
    lstData=[]
    lstSale_Data=[]
    lst_open_order=[] 
    obj1= order1.MyClass()
    while v_counter<3:
        curr_time=curr_date.time()
        print(curr_time)
        print(bln_order_placed)
        #Actual function is here. Pick list of records and submit order
        if bln_order_placed==False:
         lstObj=readcsv('D:\\Adarsh\\sharedfile\\trade-stock.csv')
         print(lstData)
         if len(lstObj)>0:
          for objY in lstObj:
           if objY.name !='' and objY.buy!="0"  and  objY.target!="0":
            if check_add_order(objY.name,objY.buy,lstData)==False:
             print("New Order Placed")
             lstData.append(objY)
             activeOrderId=obj1.place_NSE_Order(objY.name,objY.buy,objY.quantity)  
             
             bln_order_placed=True

        else:
           #Check list of open order and place the target corresponding to securityId
            obj1= order1.MyClass()
            myPosition=obj1.getPositions()
            for item1 in myPosition:
              if is_status_traded_buy(item1['status'])==True:
                if item1['securityId'] not in lst_open_order:
                 lst_open_order.append(item1['securityId'])

            
            for objY in lstData:
                if objY.name in lst_open_order:
                 if objY.name not in lstSale_Data:
                    print("sale order placed")
                    if objY.is_option=='Y':
                     activeOrderId=obj1.place_NSE_Option_Order_Sell(objY.name,objY.target,objY.quantity)                     
                    else:
                     activeOrderId=obj1.place_NSE_Order_Sell(objY.name,objY.target,objY.quantity)
                    #place sale order of security
                    lstSale_Data.append(objY.name)

            # else:
            #    #make sure that all the open position is closed
            # check ltp and if stoploss condition meet then modify sale order
            #    if is_open_position()==False:

        time.sleep(10)
    print("Time's up!")


def is_status_traded_buy(_status):
   if _status!='OPEN' and _status!='COMPLETE' and _status!='CANCELED' and _status!='REJECTED':
      return True
   else:
      return False
   
#Traded Open Order buy only
def is_buy_position_open(stockName):
   obj1= order1.MyClass()
   myPosition=obj1.getPositions()
   for item1 in myPosition:
      if is_status_traded_buy(item1['status']):
         if item1['securityId']==stockName:
            return True
   return False


#order to be place only once
def check_add_order(stockName,buyPrice,myList):
   found = False
   for item in myList:
       if item.name == stockName and item.buy==buyPrice:
           found = True
           break
   return found

#traded open order sale only
def is_sale_position_open():
   obj1= order1.MyClass()
   myPosition=obj1.getPositions()
   for item1 in myPosition:
      if item1['positionType']!='CLOSED':
            return True
   return False

#return list of stocks to be trade
def readcsv(path):
    # Create an empty list
    my_array = []    
    with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
         print(row)
         xObj = DomClass()
         xObj.name = row[0]
         xObj.buy = row[1]
         xObj.target = row[2]
         xObj.stoploss = row[3]
         xObj.quantity=row[4]
         my_array.append(xObj)
    return my_array


curr_date=datetime.now()
v_counter=0  
 
countdown()

