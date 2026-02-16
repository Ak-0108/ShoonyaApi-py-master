import time
import pandas as pd
import csv
import order1
from dom import DomClass,PositionDOM,SupportDOM
import datetime
from file_manager import MyConfigReader
import csv_manager
import os
import sound_data
import connection


os.system(f'title Internet_Order_Traded')
objConfig=MyConfigReader()
root_folder=objConfig.root_web_folder
#root_folder="D:\\Adarsh\\webfile\\"
web_url="http://mstocktrade.in/api/"
nifty_breakout_data=web_url+"nifty_breakout.php" 
 
#Checking Connection Error
check_Connection_Error=connection.MyAPIConnection()
if check_Connection_Error.ret==None:
   print("Connection API Error! Shoonya!")
   sound_data.play_sound("Connection API Error! Shoonya!")
   exit()
# End of connection check   

#Stock TradeType=CNC, FNO TradeType=NORMAL
db_option_file= root_folder+ "trade-master-fno.csv" #created based on admin setting
db_stocks_file= root_folder + 'trade-master-stock.csv'   #created based on admin setting


def countdown():  
     lstData=[]  

     #activeOrderId=obj1.place_NSE_Option_Order_Sell('NIFTY26JUN25P24800',70,75)
     v_int=0  
     while v_counter<3:
        #Actual function is here    
         #os.system('cls')
            
         #CE or PE to be entered by admin 
         lst_options=readcsv_option(db_option_file)   
         if lst_options is not None:      
          for objY2 in lst_options:
          #if check_add_order(objY.name,objY.buy,lstOrder)==False:
           if check_add_order(objY2.name,objY2.mobile)==False:         
              #if checkBuy_Order(objY2.name)==True: #If there is already  order placed then not buy order
                    data_insert= order1.MyClass() 
                    print("Option Order Placed")
                    v_int=v_int+1
                    print("Trade" +str(v_int))                    
                    activeOrderId=data_insert.place_NSE_Option_Order(objY2.name,objY2.buy,objY2.quantity) 
                    sound_data.play_sound("NIFTY Buy Order Done!")
                    lstData.append(objY2)
                    csv_data=[objY2.name,objY2.buy,objY2.target,objY2.stoploss,objY2.quantity,objY2.mobile,'NFO']
                    csv_manager.write_order_csv(csv_data)

            #END OF CHECK ORDER


        #Trade Stock Only   
         lst_stocks=readcsv_stock(db_stocks_file)  
         if lst_stocks is not None:        
          for stockObj in lst_stocks:
           if stockObj.name!='' and stockObj.buy!="0":
            if check_add_order(stockObj.name,stockObj.mobile)==False:
              #if checkBuy_Order(stockObj.name)==True:
                        data_insert= order1.MyClass()
                        print("Stock Order Placed")
                        print("Trade" +str(v_int)) 
                        activeOrderId=data_insert.place_NSE_Order(stockObj.name,stockObj.buy,stockObj.quantity) 
                        sound_data.play_sound("STOCK Buy Order Done!")
                        lstData.append(stockObj) 
                        csv_data=[stockObj.name,stockObj.buy,stockObj.target,stockObj.stoploss,stockObj.quantity,stockObj.mobile,'NSE']
                        csv_manager.write_order_csv(csv_data)              
         
        

        #wait for 10 second
         time.sleep(10)
         #Sale Order
         sale_web_trade()
         time.sleep(10)
         curr_time=curr_date.now().time()
         print(curr_time)
    #  j=0
    #  while j<2:
    #     sale_web_trade()

     print("Place Enter to Close!")


  
#order to be place only once
def check_add_order(stockName,mobile):
   found = False
   myList=csv_manager.read_order_csv()
   for item in myList:
       if item.name == stockName and item.mobile==mobile:
           found = True
           break
   return found

def checkBuy_Order(stockName):  
    var_bln=True
    obj1=order1.MyClass()
    myList=obj1.getOrderList() # order type=buy
    if myList is not None:
     for item in myList:
       if stockName== item['tsym']:
        if  item['status']=='OPEN' and item['trantype']=='B' :
          print("Buy Order: ")
          print(item) #norenordno
          var_bln=False
          break 

    return var_bln



def readcsv_option(path):
   xlistStock =[]    
   if os.path.exists(path):   
     with open(path,'r', newline='') as file:
        csvreader = csv.reader(file, delimiter=',')
        #print(f"Header: {header}")      
        for row in csvreader:             
            if len(row)==0:
               continue
            xObj = DomClass()
            xObj.expiry_dt = row[1]
            xObj.cepe_type = row[2]
            xObj.strike_rate = row[3]     
            xObj.buy = float(row[4])
            xObj.target = float(row[5])       
            xObj.stoploss = row[6]
            xObj.quantity=row[7]
            xObj.mobile=row[8]
            xObj.name=row[0]
            xlistStock.append(xObj)
            print(f"Stock: {xObj.name}, Buy: {xObj.buy}, Target: {xObj.target}, StopLoss: {xObj.stoploss}")
            
     return xlistStock

def readcsv_stock(path):
    xlistStock =[]   
    if os.path.exists(path):      
     with open(path, 'r', newline='')as file:
        csvreader = csv.reader(file, delimiter=',')
        #print(f"Header: {header}")      
        for row in csvreader:
            if len(row)==0:
               continue
            xObj = DomClass()
            xObj.name = row[0]            
            xObj.buy = float(row[1])
            xObj.target = float(row[2])       
            xObj.stoploss = row[3]
            xObj.quantity=row[4] 
            xObj.averaging_count= row[5]            
            xlistStock.append(xObj)
            print(f"Stock: {xObj.name}, Buy: {xObj.buy}, Target: {xObj.target}, StopLoss: {xObj.stoploss}")
            
    return xlistStock


def readcsv_support(path):
    xlist =[] 
    with open(path, 'r', newline='')as file:
        csvreader = csv.reader(file,delimiter=',')
        #header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
         if len(row)==0:
               continue
         xObj=SupportDOM()
         xObj.support = float(row[0])
         xObj.resistance =float(row[1])         
        
         xlist.append(xObj)
    return xlist

def checkSaleOrder(stockName):  
    var_bln=True
    var_sale= csv_manager.read_sale_order_detail_csv(stockName)
    if var_sale.name!='':
       var_bln=False

    # obj1=order1.MyClass()
    # myList=obj1.getOrderList() # order type=sale
    # if myList is not None:
    #  for item in myList:
    #   #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
    #    if  item['status']=='OPEN' and item['trantype']=='S' and stockName== item['tsym']:
    #       print("Sale Order: ")
    #       print(item) #norenordno
    #       var_bln=False
    #       break       
    return var_bln



def get_positions():
        obj1= order1.MyClass()
        myPosition=obj1.getPositions()
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
            print(f'Stocks Position List: {varOP.name}')
            lstPosition_temp.append(varOP)
        return lstPosition_temp


def sale_web_trade():
  #Get Positions
        lstPosition=get_positions()
         #sell order check position
        if len(lstPosition)>0:
          #place sale order
          for item in lstPosition:
            balance_qty=float(item.netqty)
            if balance_qty>0:
                csv_item=csv_manager.read_order_detail_csv(item.name) #check target price from csv
                if csv_item.name==item.name: #means option/stock buy is in position 
                    if checkSaleOrder(csv_item.name)==True: 
                        #write for log purpose
                        csv_data=[item.name,csv_item.target,item.netqty,csv_item.mobile,item.exch]
                        csv_manager.write_sale_order_csv(csv_data)  
                        #actual order
                        obj_sale= order1.MyClass()
                        if item.exch=="NFO":
                         print(item.name+" FNO Placed!")
                         activeOrderId=obj_sale.place_NSE_Option_Order_Sell(item.name,csv_item.target,item.netqty)
                         sound_data.play_sound("NIFTY Sale Order Done ")
                        else:
                           print(item.name+" Stock Placed!")
                           activeOrderId=obj_sale.place_NSE_Order_Sell(item.name,csv_item.target,item.netqty)
                           sound_data.play_sound("Stock Sale Order Done!")
               
                           
                            
        
        #wait for 10 second
        time.sleep(10)

curr_date=datetime.datetime.now()
v_counter=0    
countdown()