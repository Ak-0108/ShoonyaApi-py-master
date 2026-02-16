from api_helper import ShoonyaApiPy, get_time
import datetime
import logging
import time
import yaml
import pyotp
import pandas as pd
from connection import MyAPIConnection

#sample
logging.basicConfig(level=logging.DEBUG)

#flag to tell us if the websocket is open
socket_opened = False

#application callbacks
def event_handler_order_update(message):
    print("order event: " + str(message))


def event_handler_quote_update(message):
    #e   Exchange
    #tk  Token
    #lp  LTP
    #pc  Percentage change
    #v   volume
    #o   Open price
    #h   High price
    #l   Low price
    #c   Close price
    #ap  Average trade price

    print("quote event: {0}".format(time.strftime('%d-%m-%Y %H:%M:%S')) + str(message))
    

def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')
    
    api.subscribe('NSE|11630')
    #api.subscribe(['NSE|22', 'BSE|522032'])

#end of callbacks

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)

#start of our program
con_obj=MyAPIConnection()
api = ShoonyaApiPy()
api=con_obj.get_api_connection()


#use following if yaml isnt used
#user    = <uid>
#pwd     = <password>
#factor2 = <2nd factor>
#vc      = <vendor code>
#apikey  = <secret key>
#imei    = <imei>

#ret = api.login(userid = user, password = pwd, twoFA=factor2, vendor_code=vc, api_secret=apikey, imei=imei)

#yaml for parameters
with open('cred.yml') as f:
    #cred = yaml.load(f, Loader=yaml.FullLoader)
    #print(cred)

#ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA= pyotp.TOTP(cred['factor2']).now(), vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])
 if api._NorenApi__accountid is not None:  
    while True:
        print('f => find symbol')    
        print('m => get quotes')
        print('p => contract info n properties')    
        print('v => get 1 min market data')
        print('t => get today 1 min market data')
        print('d => get daily data')
        print('o => get option chain')
        print('s => start_websocket')
        print('q => quit')

        prompt1=input('what shall we do? ').lower()                    
        
        if prompt1 == 'v':
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
            
            start_secs = get_time(start_time1)
           

            ret = api.get_time_price_series(exchange='NSE', token='26000', starttime=start_secs, endtime=end_time1, interval=5)
            
            df = pd.DataFrame.from_dict(ret)
            print(df)            
            
        elif prompt1 == 't':
            ret = api.get_time_price_series(exchange='NFO', token='71321')
            
            df = pd.DataFrame.from_dict(ret)
            print(df)                        

        elif prompt1 == 'f':
            exch  = 'MCX'
            query = 'CRUDEOILM18JUN25'
            ret = api.searchscrip(exchange=exch, searchtext=query)
            print(ret)

            if ret != None:
                symbols = ret['values']
                for symbol in symbols:
                    print('{0} token is {1}'.format(symbol['tsym'], symbol['token']))

        elif prompt1 == 'd':
            exch  = 'NSE'
            tsym = 'SBIN-EQ'
             #prepare the data
            week_ago = datetime.date.today() - datetime.timedelta(days=5)
            startdate = datetime.datetime.combine(week_ago, datetime.datetime.min.time()).timestamp()          
            enddate = datetime.datetime.now().timestamp()
            ret = api.get_daily_price_series(exchange=exch, tradingsymbol=tsym, startdate=startdate,enddate=enddate)
            print(ret)
        elif prompt1 == 'df':
            exch  = 'NFO'
            tsym = '62407'
             #prepare the data
            week_ago = datetime.date.today() - datetime.timedelta(days=5)
            startdate = datetime.datetime.combine(week_ago, datetime.datetime.min.time()).timestamp()          
            enddate = datetime.datetime.now().timestamp()
            ret = api.get_daily_price_series(exchange=exch, tradingsymbol=tsym, startdate=startdate,enddate=enddate)
            print(ret)

        elif prompt1 == 'p':
            exch  = 'NSE'
            token = 'NIFTY INDEX'
            ret =  api.get_option_chain(exchange=exch, tradingsymbol=token, strikeprice=25100, count=2)
            print(ret)

        elif prompt1 == 'm':
            exch  = 'NFO'
            token = '62407' #Get PE price
            ret = api.get_quotes(exchange=exch, token=token)
            print(ret)

        elif prompt1 == 'o':
            exch  = 'MCX'
            tsym = 'CRUDEOIL18FEB22'
            chain = api.get_option_chain(exchange=exch, tradingsymbol=tsym, strikeprice=4150, count=2)

            chainscrips = []
            for scrip in chain['values']:
                scripdata = api.get_quotes(exchange=scrip['exch'], token=scrip['token'])
                chainscrips.append(scripdata)

            print(chainscrips)

        elif prompt1 == 's':

            if socket_opened == True:
                print('websocket already opened')
                continue

            ret = api.start_websocket(order_update_callback=event_handler_order_update, subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback)
            print(ret)

        else:
            ret = api.logout()
            print(ret)
            print('Fin') #an answer that wouldn't be yes or no
            break

    