import csv
import os


from dom import DomClass,DomClass_CE_PE

#v_option_file="D:/Adarsh/ShoonyaApi-py-master/db/order.csv"

#******Write single field***************
def write_single_field(new_data,file_name):
    try:
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_data)
        print("Data appended successfully to example.csv")
    except IOError:
        print("Error: Could not open or write to the file.")


def read_single_field(file_name):
    xlOrders=[]
    try:
        if os.path.exists(file_name)==False:
            return xlOrders
           
        with open(file_name, mode='r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
             print(f"Data Row: {row}")
             if len(row)==0:
               continue
             xlOrders.append(row[0])  
               
    except IOError:
        print("Error: Could not open or read the file.")

    return xlOrders

#*******Read single field***********

def write_order_csv(new_data):
    try:
        with open('db/order.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_data)
        print("Data appended successfully to example.csv")
    except IOError:
        print("Error: Could not open or write to the file.")

def write_sale_order_csv(new_data):
    try:
        with open('db/sale_order.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_data)
        print("Data appended successfully to example.csv")
    except IOError:
        print("Error: Could not open or write to the file.")


def read_order_csv():
    xlOrders=[]
    try:
        if os.path.exists('db/order.csv')==False:
            return xlOrders
           
        with open('db/order.csv', mode='r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
             print(f"Data Row: {row}")
             if len(row)==0:
               continue
                # if len(row)==0:
                #     break
             xObj = DomClass()
             xObj.name = row[0]    
             xObj.buy = row[1] 
             xObj.target = row[2]  
             xObj.stoploss = row[3]  
             xObj.quantity = row[4]  
             xObj.mobile = row[5]    
             xlOrders.append(xObj)  
               
    except IOError:
        print("Error: Could not open or read the file.")

    return xlOrders


#Write Call Put
def read_call_put_csv():
    xlOrders=[]
    try:
        if os.path.exists('db/diary.csv')==False:
            return xlOrders
           
        with open('db/diary.csv', mode='r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
             print(f"Data Row: {row}")
             if len(row)==0:
               continue
            xObj = DomClass_CE_PE()
            xObj.cepe_type = row[0]         
            xObj.is_buy = int(row[1])
            xObj.stop = int(row[2])       
            xObj.mobile=row[3]

            xlOrders.append(xObj)  
               
    except IOError:
        print("Error: Could not open or read the file.")

    return xlOrders

def write_call_put_csv(new_data):
    try:
        with open('db/diary.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_data)
        print("Data appended successfully to example.csv")
    except IOError:
        print("Error: Could not open or write to the file.")

#End Call Put


def read_order_detail_csv(stockname):
    xObj = DomClass()
    try:
        if os.path.exists('db/order.csv')==False:
          return xObj

        with open('db/order.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row)==0:
                    break
                if stockname==row[0]:
                    xObj.name = row[0]    
                    xObj.buy = row[1] 
                    xObj.target = row[2]  
                    xObj.stoploss = row[3]  
                    xObj.quantity = row[4]  
                    xObj.mobile = row[5]
                    break
               
    except IOError:
        print("Error: Could not open or read the file.")

    return xObj

def read_sale_order_csv():
    xlOrders=[]
    try:
        if os.path.exists('db/sale_order.csv')==False:
           return xlOrders
        
        with open('db/sale_order.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row)==0:
                    break
                xObj = DomClass()
                xObj.name = row[0]    
                xObj.target = row[1]  
                xObj.quantity = row[2]  
                xObj.mobile = row[3]
                xObj.exch= row[4]    
                xlOrders.append(xObj)                  
    except IOError:
        print("Error: Could not open or read the file.")

    return xlOrders

def read_sale_order_detail_csv(stockName):
    xObj = DomClass()
    try:
        if os.path.exists('db/sale_order.csv')==False:
           return xObj

        with open('db/sale_order.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row)==0:
                    break
                if stockName==row[0]:                
                    xObj.name = row[0]    
                    xObj.target = row[1]  
                    xObj.quantity = row[2]  
                    xObj.mobile = row[3]
                    xObj.exch= row[4]
                    break    
                                 
    except IOError:
        print("Error: Could not open or read the file.")

    return xObj

def read_web_data_csv(file_path):
    xlOrders=[]
    try:
        if os.path.exists(file_path)==False:
           return xlOrders
        
        with open(file_path, 'r') as file:
         content = file.read()
        
        return content         
               
    except IOError:
        print("Error: Could not open or read the file.")

    return xlOrders
