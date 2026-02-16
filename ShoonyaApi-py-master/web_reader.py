import requests
import json
import csv
from dom import DomClass,CEPENamingRule,DomClass_CE_PE


def readweb_options(web_url,db_option_file):
    api_url=web_url+"trade-master-fno.php"
    xlistStock =[]     
    response = requests.get(api_url)
    xlist_csv=[]
    if response.status_code == 200:
        
        data = response.json()
        for row in data:
            xObj = DomClass()
            xObj.expiry_dt = row['ExpiryDt']
            xObj.cepe_type = row['CallPutType']
            xObj.strike_rate = row['StrikePrice']     
            xObj.buy = float(row['BuyPrice'])
            xObj.target = float(row['SalePrice'])       
            xObj.stoploss = row['StopLoss']
            xObj.quantity=row['Quantity']
            xObj.mobile=row['Mobile']
            xObj.name=CEPENamingRule.get_cepe_name_shoonya(xObj.expiry_dt,xObj.strike_rate,xObj.cepe_type)

            v_itgem=[str(xObj.name) ,str(xObj.expiry_dt),str(xObj.cepe_type),str(xObj.strike_rate),str(xObj.buy),str(xObj.target),str(xObj.stoploss),str(xObj.quantity),str(xObj.mobile)]
            xlist_csv.append(v_itgem)

            xlistStock.append(xObj)
    else:
        print(f"Error: Could not retrieve data. Status code: {response.status_code}")

    if len(xlist_csv)>0:
        write_web_requested_data(xlist_csv,db_option_file)
    return xlistStock

def readweb_stocks(web_url,db_file):
    api_url=web_url+"trade-master-stock.php"
    xlistStock =[]     
    response = requests.get(api_url)
    xlist_csv=[]
    if response.status_code == 200:
        data = response.json()
        for row in data:
            xObj = DomClass()
            xObj.name = row['StockName']              
            xObj.buy = float(row['BuyPrice'])
            xObj.target = float(row['SalePrice'])       
            xObj.stoploss = row['StopLoss']
            xObj.quantity=row['Quantity']
            xObj.mobile=row['Mobile']   
            v_itgem=[xObj.name ,xObj.buy,xObj.target,xObj.stoploss,xObj.quantity,xObj.mobile] 
                   
            xlist_csv.append(v_itgem) 
            xlistStock.append(xObj)
    else:
        print(f"Error: Could not retrieve data. Status code: {response.status_code}")

    if len(xlist_csv)>0:
        write_web_requested_data(xlist_csv,db_file)
        
    return xlistStock


def readweb_ce(api_url,db_file):       
    response = requests.get(api_url)
    xlist_csv=[]
    if response.status_code == 200:
        data = response.json()
        for row in data:
            xObj = DomClass_CE_PE()
            xObj.cepe_type = 1            
            xObj.is_buy = 1
            xObj.stop = int(row['stop'])       
            xObj.mobile=row['Mobile']   
                 
            xlist_csv.append(xObj) 
    else:
        print(f"Error: Could not retrieve data. Status code: {response.status_code}")

    if len(xlist_csv)>0:
        write_web_requested_data(xlist_csv,db_file)
    return xlist_csv


def readweb_pe(api_url,db_file):       
    response = requests.get(api_url)
    xlist_csv=[]
    if response.status_code == 200:
        data = response.json()
        for row in data:
            xObj = DomClass_CE_PE()
            xObj.cepe_type = 2            
            xObj.is_buy = 1
            xObj.stop = int(row['stop'])       
            xObj.mobile=row['Mobile']   
                 
            xlist_csv.append(xObj) 
    else:
        print(f"Error: Could not retrieve data. Status code: {response.status_code}")

    if len(xlist_csv)>0:
        write_web_requested_data(xlist_csv,db_file)
    return xlist_csv



def write_web_requested_data(new_data,rootPath):
    try:
        
        with open(rootPath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_data)      
    except IOError:
        print("Error: Could not open or write to the file.")