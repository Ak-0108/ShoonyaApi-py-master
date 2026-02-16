from api_helper import ShoonyaApiPy
import yaml
import pyotp


class MyClass:
    def __init__(self):
        with open('cred.yml') as f:
         cred = yaml.load(f, Loader=yaml.FullLoader)
         #print(cred)
        try:
         self.api = ShoonyaApiPy()
         ret = self.api.login(userid = cred['user'], password = cred['pwd'], twoFA= pyotp.TOTP(cred['factor2']).now(), vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])
         print('Connected User: '+ ret['uname'] +' '+ ret['email'])
        except Exception as e:
         print(f"An error occurred: {e}")
        
  
    def place_NSE_Order(self,trdsymbol,price,qty):
        ret1 = self.api.place_order(buy_or_sell='B', product_type='C',
                        exchange='NSE', tradingsymbol=trdsymbol, 
                        quantity=qty, discloseqty=0,price_type='LMT', price=price, trigger_price=None,
                        retention='DAY', remarks='my_order_001')
          
        print(ret1)
        if ret1 is not None:
            return ret1['norenordno']
        else:
           return None

    def place_NSE_Order_Sell(self,trdsymbol,pprice,qty):
        ret1 = self.api.place_order(buy_or_sell='S', product_type='C',
                        exchange='NSE', tradingsymbol=trdsymbol, 
                        quantity=qty, discloseqty=0,price_type='LMT', price=pprice, trigger_price=None,
                        retention='DAY', remarks='my_order_001')    
        print("Sell Order Placed:")
        print(ret1)
    
    #'NIFTY26JUN25P24800'
    #****Intraday********
    def place_NSE_Option_Order(self,trdsymbol,pprice,qty):
        ret1 = self.api.place_order(buy_or_sell='B', product_type='I',
                        exchange='NFO', tradingsymbol=trdsymbol,  
                        quantity=qty, discloseqty=0,price_type='LMT', price=pprice, trigger_price=None,
                        retention='DAY', remarks='my_order_001')
        if ret1 is not None:
            return ret1['norenordno']
        else:
           return None

  
    def place_NSE_Option_Order_Sell(self,trdsymbol,pprice,qty):
        f=self.api.place_order(buy_or_sell='S', product_type='I',
                        exchange='NFO', tradingsymbol=trdsymbol, 
                        quantity=qty, discloseqty=0,price_type='LMT', price=pprice, trigger_price=None,
                        retention='DAY', remarks='my_order_001')     
        print("Sell Order Placed:")
        print(f)

    def place_NSE_Option_Market(self,trdsymbol,qty):
        ret1 = self.api.place_order(buy_or_sell='B', product_type='I',
                        exchange='NFO', tradingsymbol=trdsymbol,  
                        quantity=qty, discloseqty=0,price_type='MKT', price=0,  trigger_price=None,
                        retention='DAY', remarks='my_order_001')
        if ret1 is not None:
            return ret1['norenordno']
        else:
           return None

    
    def place_NSE_Option_Market_Sell(self,trdsymbol,qty):
        f=self.api.place_order(buy_or_sell='S', product_type='I',
                        exchange='NFO', tradingsymbol=trdsymbol, 
                        quantity=qty, discloseqty=0,price_type='MKT', price=0, trigger_price=None,
                        retention='DAY', remarks='my_order_001')     
        print("Sell Order Placed:")
        print(f)

    #****Intraday* END*******

    def place_NSE_Option_Market_Order(self,trdsymbol,qty):
        ret1 = self.api.place_order(buy_or_sell='B', product_type='I',
                        exchange='NFO', tradingsymbol=trdsymbol,  
                        quantity=qty, discloseqty=0,price_type='MKT', trigger_price=None,
                        retention='DAY', remarks='my_order_001')
        return ret1
        
    def place_NSE_Option_MarketOrder_Sell(self,trdsymbol,qty):
        f=self.api.place_order(buy_or_sell='S', product_type='I',
                        exchange='NFO', tradingsymbol=trdsymbol, 
                        quantity=qty, discloseqty=0,price_type='MKT', trigger_price=None,
                        retention='DAY', remarks='my_order_001')     
        print("Sell Order Placed:")
        print(f)

    def place_MCX_Order(self,trdsymbol,pprice,qty):
        f=self.api.place_order(buy_or_sell='B', product_type='M',
                        exchange='MCX', tradingsymbol=trdsymbol, 
                        quantity=qty, discloseqty=0,price_type='LMT', price=pprice, trigger_price=None,
                        retention='DAY', remarks='my_order_001')     
        print("Buy Order Placed:")
        print(f)


# # Fetch all orders
    def getOrderList(self):
     d=self.api.get_order_book()
     return d

# # Get order by id
    def getOrderById(self,order_Id):
     d=self.api.single_order_history(orderno=order_Id)
     return d
    
  
    # Get positions
    def getPositions(self):
     d=self.api.get_positions()
     return d
    
    # Get positions
    def getHoldings(self):
     d=self.api.get_holdings()
     print(d)
     

# # Modify order
    def modify_order(self,order_id_old,pprice):
        f=self.api.modify_order(exchange='NSE',  orderno=order_id_old,
                                    newprice_type='LMT', newprice=pprice)     
        print("Order Modified:")
        print(f)
    
    # # Modify Target Order
    def cancel_Order(self,order_id_old):
        f=self.api.cancel_order(orderno=order_id_old)     
        print("Order Canceled:")
        print(f)


def __del__(self):
 print("Object is being destroyed")
