import time
import order1
from datetime import datetime
from dom import PositionDOM
from get_price_cls import PriceReaderClass
import dom_strike
import csv_manager


quanity_nifty=75
quanity_bank_nifty=30
lst_sale_order=[]
lst_sale_item=[] #used to check sell order

def Main(): 
     
    lstData=[]
    lst_open_order=[] 
    obj1=PriceReaderClass()

    nifty_ltp= dom_strike.get_nifty_ltp()
    cedone=False
    pedone=False 
    expiry_month=dom_strike.get_current_expiry()
    #expiry_month=dom_strike.get_next_expiry()
    i=0
    while i<5:     
      cedone=function_sell(nifty_ltp,expiry_month)

      time.sleep(5)
    print("Time's up!")
    
     

def function_sell(nifty_ltp, expiry_month):   
            pe_strike=dom_strike.calculate_atm_put(nifty_ltp)
            pe_name=dom_strike.get_pe_name_strike(expiry_month,pe_strike)  
            #above is only once in a day cycle

            pe_buy_price=dom_strike.get_nifty_pe_rate(pe_strike,expiry_month) #obj1.read_ce_pe_rate(pe_name)
            print(f'Buy Put '+  pe_name +' at: ' +str(pe_buy_price))
            #Order submission
            
            v_buy_done= csv_manager.read_single_field('db/pe_order_market.csv')
            if len(v_buy_done)==0:
            #Order submission
                submit_buy_order(ce_pe_name=pe_name,buy_price=pe_buy_price)
                csv_data=[pe_name]
                csv_manager.write_single_field(csv_data,'db/pe_order_market.csv')



#Buy Actual Trade
def submit_buy_order(ce_pe_name,buy_price):
    data_insert= order1.MyClass() 
    print(ce_pe_name +" submitted!")
    activeOrderId=data_insert.place_NSE_Option_Market(ce_pe_name,buy_price,quanity_nifty)  


def sale_order(cepe_name):
     lstPosition=get_positions()
     if len(lstPosition)>0:
          #place sale order
          for item in lstPosition:
            balance_qty=float(item.netqty)
            if balance_qty>0:  
                v_buy_done= csv_manager.read_single_field('db/sale_pe_order_market.csv')
                if len(v_buy_done)==0:
                    if checkSaleOrder(item.name)==True: 
                        obj_sale= order1.MyClass()
                        activeOrderId=obj_sale.place_NSE_Option_Market_Sell(cepe_name,item.daybuyqty)
                        print(item.name+" Sale Order done!")
                        csv_data=[item.name]
                        csv_manager.write_single_field(csv_data,'db/sale_pe_order_market.csv')


def checkSaleOrder(stockName):  
    var_bln=True
    try:
        obj1=order1.MyClass()
        myList=obj1.getOrderList() # order type=sale
        if myList is not None:
            for item in myList:
        #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
                if  item['status']=='OPEN' and item['trantype']=='S' and stockName== item['tsym']:
                    print(item) #norenordno
                    var_bln=False
                    break  

    except Exception as e:
       print(f"An error occurred: {e}")
            
    return var_bln

  

def get_positions():
    lstPosition_temp=[]
    try:
        obj1= order1.MyClass()
        myPosition=obj1.getPositions()
        print(myPosition)
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
            print(varOP.name)
            lstPosition_temp.append(varOP)
    except Exception as e:
        print(f"An error occurred: {e}")

    return lstPosition_temp


curr_date=datetime.now()
v_counter=0  
 
Main()

