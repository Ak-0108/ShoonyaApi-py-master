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
plateform_price_reader=PriceReaderClass()
stock_name="IRFC-EQ"

# Read list of stocks from CSV 
# Submit Buy Order based on OHLC

#get previous chart just before current
def get_prev_chart(nifty_chart):
    obj=PricekDOM()
    i=0
    for row in nifty_chart.itertuples():
        #0 mean current chart, 1 mean previous chart
        if i>1:
            break
        if i==1:
        #print(f"Index: {row.Index}, Col1: {row.into}, Col2: {row.intc}")
            obj.open=float(row.into)
            obj.close=float(row.intc)
            obj.high=float(row.inth)
            obj.low=float(row.intl)
            obj.time=row.time
        i=i+1
    return obj

#get current chart
def get_chart_rate(nifty_chart):
    obj=PricekDOM()
    i=0
    for row in nifty_chart.itertuples():
        if i>0:
            break
        #print(f"Index: {row.Index}, Col1: {row.into}, Col2: {row.intc}")
        obj.open=float(row.into)
        obj.close=float(row.intc)
        obj.high=float(row.inth)
        obj.low=float(row.intl)
        obj.time=row.time
        i=i+1
    return obj

def get_prev2ndchart(nifty_chart):
    obj=PricekDOM()
    i=0
    #0 mean current chart, 1 mean previous chart
    for row in nifty_chart.itertuples():
        if i>2:
            break
        #print(f"Index: {row.Index}, Col1: {row.into}, Col2: {row.intc}")
        if i==2:
            obj.open=float(row.into)
            obj.close=float(row.intc)
            obj.high=float(row.inth)
            obj.low=float(row.intl)
            obj.time=row.time
        i=i+1
    return obj

def read_one_minute_chart(objRead):
    chart_previous = datetime.datetime.now() - datetime.timedelta(minutes=1)
    nifty_1min=objRead.read_nifty_chart_start_from(chart_previous,1)
    data_1min=get_chart_rate(nifty_1min)
    return data_1min

#start of 5 min chart trade
def trade_with_5min_chart(stockName1):
    objRead=PriceReaderClass()
    nifty_5min=objRead.read_stock_daily_chart(stockName1)
    print("Stock Daily chart:")
    print(nifty_5min)
  
    return nifty_5min
# End of 5 min chart trade


#start of 15 min chart trade
def trade_with_15min_chart(ce_name,pe_name):
    current_time_only = datetime.datetime.now().time()
    specific_time = datetime.time(9, 45, 0)  # 11 PM, 30 minutes, 15 seconds
    t_done_var=False
    if current_time_only>=specific_time:   
        objRead=PriceReaderClass()
        nifty_15min=objRead.read_nifty_chart(15)
        print("Nifty 15min chart:")
        print(nifty_15min)        
        #starting 15min chart logic
        data=get_chart_rate(nifty_15min) #1st candle
        data_prev=get_prev_chart(nifty_15min) #2nd candle previous

        nifty_5min=objRead.read_nifty_chart(5) #5min candle
        prev_5_1=get_chart_rate(nifty_5min) # current candle

        if data_prev.close>data_prev.open: #prev candle is green
            if data.close>data.open:
                #confirm green candle
                buy_p_15=objRead.read_ce_pe_rate(ce_name)
                print("Buy 15min Call at Price: "+ str(buy_p_15) )
                #actual buy order

            if prev_5_1.close>prev_5_1.open: #green is also at 5min
                buy_p_15_5=objRead.read_ce_pe_rate(ce_name)
                print("Buy 15min&5min Call at Price: "+ str(buy_p_15_5) )

            #Red candle logic
        if data_prev.close<data_prev.open: #prev candle is red
            if data.close<data.open:
                #confirm red candle
                buy_p_15=objRead.read_ce_pe_rate(pe_name)
                print("Buy 15min Put at Price: "+ str(buy_p_15) )
                #actual buy order   
            
            if prev_5_1.close<prev_5_1.open: #current 5min candle is red
                #confirm green candle
                buy_p_15_5=objRead.read_ce_pe_rate(pe_name)
                print("Buy 15min_5min Put at Price: "+ str(buy_p_15_5) )
                #actual buy order     
        

        #start to check 5min        
        prev_5_2=get_prev_chart(nifty_5min) # prev candle 5min
        
        if data.close>data.open: #green candle 15 min  
            if prev_5_1.open>prev_5_2.close:
                buy_p=objRead.read_ce_pe_rate(ce_name)
                print("Buy Call at Price: "+ str(buy_p) )
                t_done_var=True

        elif data.close<data.open: #red candle 5 min  
            if prev_5_1.open<prev_5_2.close:
                buy_p=objRead.read_ce_pe_rate(pe_name)
                print("Buy Put at Price: "+ str(buy_p) )
                t_done_var=True

        return t_done_var

# End of 15 min chart trade

#start 30 min chart
def trade_dailychart(stock_name1):
    row=plateform_price_reader.read_stock_price_info(stock_name1)
    obj=PricekDOM()
        #print(f"Index: {row.Index}, Col1: {row.into}, Col2: {row.intc}")
    obj.open=float(row.open)
    obj.close=float(row.close)
    obj.high=float(row.high)
    obj.low=float(row.low)
    obj.average=float(row.average)
    obj.rate=float(row.rate)
    return obj



def trade_cpr_base(lte,stockName1):
    test_chart=trade_dailychart(stockName1)
    v_cpr=nifty_reader.calculate_cpr(test_chart.high,test_chart.low,test_chart.close)
    pv_level=float(v_cpr['Pivot'])
    pv_top=float(v_cpr['TopCentralPivot'])
    pv_bottom=float(v_cpr['BottomCentralPivot'])

    #green
    if test_chart.close > test_chart.open:
        if lte > pv_level and lte< pv_top:
            print("buy_order")#call

    #red
    if test_chart.close < test_chart.open:
        if lte < pv_level and lte < pv_bottom:
            print("sell order")#put

    #end 30 min chart


def start_trade(status_var):   
    bln_order_placed=False   
    # Get the current date and time
    current_datetime = datetime.datetime.now()
        # Print the full datetime object
    print("Current Date and Time:", current_datetime)
        # Extract and print only the time
    current_time_only = current_datetime.time()
    print("Current Time (object):", current_time_only)
    specific_time = datetime.time(9, 20, 0)  # 11 PM, 30 minutes, 15 seconds

    if current_time_only>=specific_time or 1==1: #remove 1==1 during live
        print("Start")  
        status_var.order_started=True
    
    #Calculate CE & PE 
    
        # nifty_ltp=nifty_reader.get_nifty_ltp()
        # print("NIFTY RATE: "+str(nifty_ltp))
        nifty_info=plateform_price_reader.read_stock_price_NSE(stock_name)
        nifty_ltp= float(nifty_info['lp'])
        print("IRFC RATE: "+str(nifty_ltp))
        #v_prev_day=plateform_price_reader.read_nifty_chart_start_from(,,)

        #pivot point logic
        trade_cpr_base(nifty_ltp,stock_name)

        #end logic
        #calculate based on previous day chart
        status_var.chart_5min_placed= trade_with_5min_chart(stock_name)
         
         #if current price is above 5 min chart then place buy order



def submit_buy_order(ce_pe_name):
    obj1= order1.MyClass()
    print(ce_pe_name +" submitted!")
    #activeOrderId=obj1.place_NSE_Option_Order(ce_pe_name,75) 



while status_var.order_started==False: 
    start_trade(status_var)
    time.sleep(10)


