import time
import csv
from datetime import datetime
from dom import DomClass,SupportDOM
from get_price_cls import PriceReaderClass
import nifty_reader


shoonyaPath='D:\\Adarsh\\sharedfile\\shoonya\\support.csv'
iciciPath='D:\\Adarsh\\sharedfile\\icici\\support.csv'

def countdown():   
    bln_order_placed=False    
    exp_month=nifty_reader.get_nifty_expiry() 

    obj1=PriceReaderClass()

    # Example usage with sample data (replace with your actual data)
    previous_day_high = 105.50
    previous_day_low = 100.25
    previous_day_close = 103.75

    pivot_levels = nifty_reader.calculate_pivot_points(previous_day_high, previous_day_low, previous_day_close)
    cpr_values = nifty_reader.calculate_cpr(previous_day_high, previous_day_low, previous_day_close)

    print(cpr_values)

    for level, value in pivot_levels.items():
        print(f"{level}: {value:.2f}")


    while v_counter<3:
        curr_time=datetime.now()
        print(curr_time)
        print(bln_order_placed)
        nifty_ltp=obj1.read_nifty_lte()
        strikePrice=nifty_ltp['lp']
        print(nifty_ltp)
        cename=nifty_reader.get_Shoonya_ce_name(expiry_month=exp_month,ltp=strikePrice)
        pe_buy_price=obj1.read_ce_pe_price_info(cename)
        print(pe_buy_price.rate )
        print(pe_buy_price.average )
        #Actual function is here. Pick list of records and submit order
        time.sleep(16) 

          
    print("Time's up!")


#return list of stocks to be trade
def readcsv(path):
    with open(path, mode ='r')as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print(f"Header: {header}")      
        for row in csvreader:         
         xObj = SupportDOM ()
         xObj.support = row[0]
         xObj.resistance = row[1]         
    return xObj


def writeCSV(data,strPath):
 with open(strPath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)


v_counter=0   
countdown()

