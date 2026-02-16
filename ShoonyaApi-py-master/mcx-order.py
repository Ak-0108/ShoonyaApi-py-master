from api_helper import ShoonyaApiPy, get_time
import datetime
import logging
import time
import yaml
import pyotp
import pandas as pd

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)

#start of our program
api = ShoonyaApiPy()


#yaml for parameters
with open('cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA= pyotp.TOTP(cred['factor2']).now(), vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

if ret != None:   
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
            start_time = "11-06-2025 00:00:00"
            end_time = time.time()
            
            start_secs = get_time(start_time)

            ret = api.get_time_price_series(exchange='NSE', token='22', starttime=start_secs, endtime=end_time, interval=240)
            
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
            tsym = 'RELIANCE-EQ'
            ret = api.get_daily_price_series(exchange=exch, tradingsymbol=tsym, startdate=0)
            print(ret)

        elif prompt1 == 'p':
            exch  = 'NSE'
            token = '22'
            ret = api.get_security_info(exchange=exch, token=token)
            print(ret)

        elif prompt1 == 'm':
            exch  = 'NSE'
            token = '22'
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


        else:
            ret = api.logout()
            print(ret)
            print('Fin') #an answer that wouldn't be yes or no
            break

    