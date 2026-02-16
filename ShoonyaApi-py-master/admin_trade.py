import time
import pandas as pd
import csv
import order1
from dom import DomClass,PositionDOM,SupportDOM,CEPENamingRule,OrderDOM
import datetime
from file_manager import MyConfigReader
from get_price_cls import PriceReaderClass
import order_live
import os
import subprocess


# v1=CEPENamingRule.get_cepe_admin_shoonya("2025-Aug-07","24700","CE")
# print(v1)
os.system(f'title Admin_Submit_Trade')
objConfig=MyConfigReader()
root_folder=objConfig.root_folder +"\\"

# lst_files.append("support-high.csv")
# lst_files.append("buy-range.csv")
# lst_files.append("sell-range.csv")
# above three is used by stock-auto\stockcode\nifty-support-high
# lst_files.append("trade-fno.csv")
# lst_files.append("trade-stock.csv")

manual_option_file= root_folder+ "trade-master-fno.csv" #created based on admin setting
stocks_file= root_folder + 'trade-master-stock.csv'   #created based on admin setting

def countdown():
    v_counter=0
    lstOrder=[]
    lstOrder_Pending=[]
    bln_sale_start=False   
    lstData=[]
           
     #cancel order
     #cancel_open_order(obj1)
     #end of cancel order
    obj1= order1.MyClass()
    try:
      myList=obj1.getOrderList()
      print("Open Orders:\n")
      if myList is not None:
       for item in myList:
      #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
        if  item['status']!='CANCELED' and item['status']!='REJECTED' and item['status']!='COMPLETE':
          print(item) #norenordno
          order_var=OrderDOM()
          order_var.name=item['tsym']
          order_var.exch=item['exch']
          order_var.order_id=item['norenordno']
          order_var.qty=item['qty']
          order_var.buy_sell_type=item['trantype']
          order_var.status=item['status']
          lstOrder_Pending.append(order_var)          
          lstOrder.append(item['norenordno'])
          #orderNo=item['norenordno']
          #obj1.cancel_Order(orderNo)
    except Exception as e:
     print(f"An error occurred: {e}")
   
    while v_counter<2:
        #Actual function is here     
        cnt_op=get_positions_count_options() 
        if cnt_op<=4:
         #CE or PE to be entered by admin
            manualOption=readcsv_option(manual_option_file)
            for objY2 in manualOption:
            #if check_add_order(objY.name,objY.buy,lstOrder)==False:
                if check_add_order(objY2.name,objY2.buy,lstData)==False:         
                #current_price=objPriceReader.read_ce_pe_rate(objY2.name)
                    if checkBuy_Order(objY2.name)==True:                        
                        try:
                         data_insert= order1.MyClass()
                         activeOrderId=data_insert.place_NSE_Option_Order(objY2.name,objY2.buy,objY2.quantity) 
                         if activeOrderId is not None:
                            lstData.append(objY2)
                        except Exception as e:
                         print(f"An error occurred: {e}")
        
        else:
            v_counter=v_counter+1
            #END OF CHECK ORDER


        #Trade Stock Only
        cnt_stock=get_positions_count_stocks() 
        if cnt_stock<=4:
            xlistStock=readcsv_stock(stocks_file)
            for stockObj in xlistStock:
                if stockObj.name!='' and stockObj.buy!="0":
                    if check_add_order(stockObj.name,stockObj.buy,lstData)==False:
                        if checkBuy_Order(stockObj.name)==True:
                            try:
                             data_insert= order1.MyClass()
                             activeOrderId=obj1.place_NSE_Order(stockObj.name,stockObj.buy,stockObj.quantity)  
                             if activeOrderId is not None:       
                                lstData.append(stockObj)
                            except Exception as e:
                             print(f"An error occurred: {e}")
        else:
            v_counter=v_counter+1
            #obj1.modify_order(activeOrderId,objY.buy)

        #end of while loop
        #wait for 10 second
        time.sleep(10)
        #run sale_trade py only once in a day
        if bln_sale_start==False:
            print("Sale Order Started!")
            bln_sale_start=True
            subprocess.run(["python", "sale_trade.py"]) 
            # Run without arguments

        curr_time=curr_date.time()
        print(curr_time)

    print("Place Press EnterKey to Close!")


  
#order to be place only once
def check_add_order(stockName,buyPrice,myList):
   found = False
   for item in myList:
       if item.name == stockName and item.buy==buyPrice:
           found = True
           break
   return found

def checkBuy_Order(stockName):  
    var_bln=True
    obj1=order1.MyClass()
    myList=obj1.getOrderList() # order type=buy
    if myList is not None:
     for item in myList:
       if  item['status']=='OPEN' and item['trantype']=='B' and stockName== item['tsym']:
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

#used to cancel order
def cancel_open_order(obj1):  
    myListCancel=obj1.getOrderList()
    if myListCancel is not None:
      for citem in myListCancel:
         if citem['status']=='OPEN':
          orderno=citem['norenordno']  
          obj1.cancel_Order(orderno)


def get_positions_count_options():
        var_option_count=0
        try:
            obj1= order1.MyClass()
            myPosition=obj1.getPositions()
            if myPosition is not None:
                for item1 in myPosition:
                    var_exch=item1['exch']
                    if var_exch=="NFO":
                     var_option_count=var_option_count+1  
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
          
        return var_option_count


def get_positions_count_stocks():
    var_stock_count=0
    try:
        obj1= order1.MyClass()
        myPosition=obj1.getPositions()        
        if myPosition is not None:
          for item1 in myPosition:
            var_exch=item1['exch']
            if var_exch=="NSE":
               var_stock_count=var_stock_count+1

    except Exception as e:
     print(f"An error occurred: {e}")
    
    return var_stock_count

def readcsv_option(path):
    xlistStock =[]    
    if os.path.exists(path):   
     with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        if csvreader.line_num==0:
         header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
            if len(row)==0:
               break
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

def readcsv_stock(path):
    xlistStock =[]   
    if os.path.exists(path):  
     with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        if csvreader.line_num ==0:
         header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:
            if len(row)==0:
               break
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

def readcsv_list(path):
    xlist =[] 
    if os.path.exists(path):  
     with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        if csvreader.line_num ==0:
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
    if os.path.exists(path):  
     with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        if csvreader.line_num ==0:
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
