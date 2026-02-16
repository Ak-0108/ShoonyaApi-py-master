import time
import csv
import datetime
import time
import pandas as pd
from dom import CEPENameDOM,StatusDOM,PricekDOM
import nifty_reader
from get_price_cls import PriceReaderClass
import order1

status_var=StatusDOM()
ce_pe_var=CEPENameDOM()
plateform_price_reader=PriceReaderClass()

i=0
while i==0:
    nifty_ltp_latest=plateform_price_reader.read_nifty_lte()
    print(nifty_ltp_latest['lp'])
    nifty_ltp=nifty_reader.get_nifty_ltp()
    print("NIFTY RATE: "+str(nifty_ltp))
    time.sleep(10)



def submit_buy_order(ce_pe_name):
    obj1= order1.MyClass()
    activeOrderId=obj1.place_NSE_Option_Market_Order(ce_pe_name,75) 

 