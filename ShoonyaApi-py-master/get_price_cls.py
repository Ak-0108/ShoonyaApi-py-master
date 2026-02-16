from api_helper import ShoonyaApiPy
import yaml
import pyotp
import pandas as pd
#below is for chart read
import datetime
from nsepython import *
import time
from dom import PricekDOM
from connection import MyAPIConnection

class PriceReaderClass:
    def __init__(self):
         self.api = ShoonyaApiPy()
         con_obj=MyAPIConnection()
         self.api=con_obj.get_api_connection()
  
    def read_stock_price_NSE(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='NSE', token=trdsymbol)          
        return ret1

    def read_stock_price_MCX(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='MCX', token=trdsymbol)          
        return ret1

    def read_stock_price_SENSEX(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='BSE', token=trdsymbol)          
        return ret1   
    
    def read_nifty_lte(self):
        ret1 = self.api.get_quotes(exchange='NSE', token='26000')          
        return ret1
    
    def read_banknifty_lte(self):
        ret1 = self.api.get_quotes(exchange='NSE', token='26009')          
        return ret1
    
    def read_indivix_lte(self):
        ret1 = self.api.get_quotes(exchange='NSE', token='26017')          
        return ret1
    
    # def read_nifty_daily_chart(self):
    #     ret1 = self.api.get_quotes(exchange='NSE', token='26000')          
    #     return ret1
    

    def read_nifty_chart(self,interval_min):
        var_d=datetime.date.today().weekday()
        prev_day_int=0
        if var_d<5:
         prev_day_int=0
        else:
         prev_day_int=3

        week_ago = datetime.date.today() - datetime.timedelta(days=prev_day_int)
        start_time1=week_ago.strftime("%d-%m-%Y %H:%M:%S")
        end_time1 = time.time()                    
        data = time.strptime(start_time1,'%d-%m-%Y %H:%M:%S')
        start_secs= time.mktime(data)
      
        ret = self.api.get_time_price_series(exchange='NSE', token='26000', starttime=start_secs, endtime=end_time1, interval=interval_min)
                    
        df = pd.DataFrame.from_dict(ret)
        return df   
    
    def read_nifty_chart_30min(self):
        var_d=datetime.date.today().weekday()
        #5:saturday, 6:sunday, 0:monday=
        prev_day_int=0
        if var_d==5:
         prev_day_int=1
        elif var_d==6:
            prev_day_int=2
        else:
         prev_day_int=0
        
        #hours=hh_extra2
        week_ago = datetime.date.today() - datetime.timedelta(days=prev_day_int)
        start_time1=week_ago.strftime("%d-%m-%Y %H:%M:%S")     
        print("start from: ",start_time1)            
        data = time.strptime(start_time1,'%d-%m-%Y %H:%M:%S')
        start_secs= time.mktime(data)

        end_time1 = time.time()  
      
        ret = self.api.get_time_price_series(exchange='NSE', token='26000', starttime=start_secs, endtime=end_time1, interval='30')
                    
        df = pd.DataFrame.from_dict(ret)
        return df 

    def read_nifty_chart_start_from(self,start_time,interval_min):
               
        start_time1=start_time.strftime("%d-%m-%Y %H:%M:%S")
        end_time1 = time.time()                    
        data = time.strptime(start_time1,'%d-%m-%Y %H:%M:%S')
        start_secs= time.mktime(data)
        ret = self.api.get_time_price_series(exchange='NSE', token='26000', starttime=start_secs, endtime=end_time1, interval=interval_min)
                    
        df = pd.DataFrame.from_dict(ret)
        return df   
    

    def read_banknifty_chart(self,interval_min):
        var_d=datetime.date.today().weekday()
        print(var_d)
        prev_day_int=0
        if var_d<5:
         prev_day_int=0
        else:
         prev_day_int=3

        week_ago = datetime.date.today() - datetime.timedelta(days=prev_day_int)
        start_time1=week_ago.strftime("%d-%m-%Y %H:%M:%S")
        end_time1 = time.time()                    
        data = time.strptime(start_time1,'%d-%m-%Y %H:%M:%S')
        start_secs= time.mktime(data)
        ret = self.api.get_time_price_series(exchange='NSE', token='26009', starttime=start_secs, endtime=end_time1, interval=interval_min)
                    
        df = pd.DataFrame.from_dict(ret)
        return df 
         

    def read_stock_daily_chart(self,trdsymbol):
            exch  = 'NSE'
             #prepare the data
            week_ago = datetime.date.today() - datetime.timedelta(days=5)
            startdate = datetime.datetime.combine(week_ago, datetime.datetime.min.time()).timestamp()          
            enddate = datetime.datetime.now().timestamp()
            ret = self.api.get_daily_price_series(exchange=exch, tradingsymbol=trdsymbol, startdate=startdate,enddate=enddate)
            return ret


    def read_stock_today_daily_chart(self,trdsymbol):
            exch  = 'NSE'
             #prepare the data
            week_ago = datetime.date.today()
            startdate = datetime.datetime.combine(week_ago, datetime.datetime.min.time()).timestamp()          
            enddate = datetime.datetime.now().timestamp()
            ret = self.api.get_daily_price_series(exchange=exch, tradingsymbol=trdsymbol, startdate=startdate,enddate=enddate)

    def read_ce_pe_rate(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='NFO', token=trdsymbol)          
        return ret1
    
    def read_ce_pe_price_info(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='NFO', token=trdsymbol)    
        data=PricekDOM()
        if ret1 is not None:
            data.rate= ret1['lp'] 
            data.close= ret1['c'] 
            data.high= ret1['h'] 
            data.low= ret1['l'] 
            data.open= ret1['o']   
            data.average=ret1['ap']
        return data

    def read_stock_price_info(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='NSE', token=trdsymbol)    
        data=PricekDOM()
        if ret1 is not None:
            data.rate= ret1['lp'] 
            data.close= ret1['c'] 
            data.high= ret1['h'] 
            data.low= ret1['l'] 
            data.open= ret1['o']   
            data.average=ret1['ap']
        return data
    
    def read_ce_pe_rate(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='NFO', token=trdsymbol)    
        rate=0
        if ret1 is not None:
            rate=float(ret1['lp'])            
        return rate
    
    def read_stock_rate(self,trdsymbol):
        ret1 = self.api.get_quotes(exchange='NSE', token=trdsymbol)    
        rate=0
        if ret1 is not None:
            rate=float(ret1['lp'])            
        return rate
    

def __del__(self):
 print("Object is being destroyed")
