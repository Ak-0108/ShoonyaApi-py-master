import pandas as pd
import order1
import datetime

def countdown():
     lstOrder=[]
     obj1= order1.MyClass()
    
     myList=obj1.getPositions() # order type=sale
     print("Open Orders:\n")
     if myList is not None:
      for item in myList:
        var_name=item['tsym']
        var_qty=item['daybuyqty']
        var_ltp=item['lp']
        var_netqty=float(item['netqty'])
        var_profit_amt=item['rpnl']
        
      #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
        if var_netqty>0:
          print(item) #norenordno
          obj_sale= order1.MyClass()
          #Check If Sell Order placed then modify order else 
          if item['exch']=="NFO":
              activeOrderId=obj_sale.place_NSE_Option_MarketOrder_Sell(var_name,var_qty)
          else:
              activeOrderId=obj_sale.place_NSE_Order_Sell(var_name,var_qty)

         
     print("Place Enter to Close!")


  
#square-off position
def square_off(var_name,var_qty):
        obj_sale= order1.MyClass()
        activeOrderId=obj_sale.place_NSE_Option_MarketOrder_Sell(var_name,var_qty)

#used to cancel order
def cancel_open_order(orderno):  
        obj1= order1.MyClass()
        obj1.cancel_Order(orderno)

curr_date=datetime.datetime.now()
v_counter=0    
countdown()
