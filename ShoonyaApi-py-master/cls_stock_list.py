import time
import csv
from datetime import datetime
from dom import StockDOM
from get_price_cls import PriceReaderClass


"""
This file will read price of stocks and then prepare list of stock which to be buy
"""

def countdown():     
    order_count=0
    bln_order_placed=False
    lstData=[]
    lstSale_Data=[]
    lst_open_order=[] 
    obj1=PriceReaderClass()
    dataindex=obj1.read_nifty_lte()
    print(dataindex)
    lstData.append(dataindex)
    dataindex=obj1.read_banknifty_lte()
    print(dataindex)
    lstData.append(dataindex)

    


    lstObj=readcsv('D:\\Adarsh\\sharedfile\\stock_list.csv')
    if len(lstObj)>0:
     for objY in lstObj:
      if objY !='':        
           data=obj1.read_stock_price_NSE(objY)      
         
           if data!=None:
            print(data)
            lstData.append(data)
           
    time.sleep(10)
    print("Time's up!")


   
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
         if len(row)==0:
            break
         name=row[0]
         my_array.append(name)
    return my_array


curr_date=datetime.now()
v_counter=0  
 
countdown()

