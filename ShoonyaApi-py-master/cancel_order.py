import pandas as pd
import order1
import datetime


def countdown():
     lstOrder=[]
     obj1= order1.MyClass()
    
     myList=obj1.getOrderList() # order type=sale
     print("Open Orders:\n")
     if myList is not None:
      for item in myList:
      #if item['status']!='OPEN' and item['status']!='COMPLETE' and item['status']!='CANCELED' and item['status']!='REJECTED':
       if  item['status']!='CANCELED' and item['status']!='REJECTED' and item['status']!='COMPLETE':
          print(item) #norenordno
          lstOrder.append(item['norenordno'])
          var_name=item['tsym']
          qty_open=item['qty']          
          if item['trantype']=='B':
             cancel_open_order(item['norenordno'])
          elif item['trantype']=='S':
            obj_sale= order1.MyClass()
            activeOrderId=obj_sale.place_NSE_Option_MarketOrder_Sell(var_name,qty_open)

         
     print("Place Enter to Close!")


  
#used to cancel order
def cancel_open_order(orderno):  
        obj1= order1.MyClass()
        obj1.cancel_Order(orderno)

curr_date=datetime.datetime.now()
v_counter=0    
countdown()
