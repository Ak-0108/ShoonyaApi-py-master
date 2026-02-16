from api_helper import ShoonyaApiPy
import yaml
import pyotp
import datetime
import time
import pandas as pd


class PriceReaderClass:
    def __init__(self):
        with open('cred.yml') as f:
         cred = yaml.load(f, Loader=yaml.FullLoader)
         self.api = ShoonyaApiPy()
         ret = self.api.login(userid = cred['user'], password = cred['pwd'], twoFA= pyotp.TOTP(cred['factor2']).now(), vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])
        
  
    def read_nifty_chart(self,interval_min):
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
         

    def read_nifty_daily_chart(self):
            exch  = 'NSE'
             #prepare the data
            week_ago = datetime.date.today() - datetime.timedelta(days=5)
            startdate = datetime.datetime.combine(week_ago, datetime.datetime.min.time()).timestamp()          
            enddate = datetime.datetime.now().timestamp()
            ret = self.api.get_daily_price_series(exchange=exch, tradingsymbol='26009', startdate=startdate,enddate=enddate)


    def read_stock_today_daily_chart(self,trdsymbol):
            exch  = 'NSE'
             #prepare the data
            week_ago = datetime.date.today()
            startdate = datetime.datetime.combine(week_ago, datetime.datetime.min.time()).timestamp()          
            enddate = datetime.datetime.now().timestamp()
            ret = self.api.get_daily_price_series(exchange=exch, tradingsymbol=trdsymbol, startdate=startdate,enddate=enddate)

    

def __del__(self):
 print("Object is being destroyed")
