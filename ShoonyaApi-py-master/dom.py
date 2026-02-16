import calendar
class DomClass:
    mobile=''
    expiry_dt=''
    strike_rate=''
    cepe_type=''
    name= ''
    buy= 0
    target=0
    stoploss=''
    updated=''
    quantity=''
    is_option=''
    exch=''
    averaging_count=0
    is_order_executed=False
    is_square_off=False
    is_sale_order_placed=False

class DomClass_CE_PE:
    mobile=''
    is_buy=0
    cepe_type=0
    stop= 0

class PositionDOM:
   name=''
   exch=''
   daybuyqty=0
   daysellqty=0
   netqty=0
   profit_amt=0
   ltp=0
   daybuyavgprc=0
   daysellavgprc=0
   qty=0

class StockDOM:
   name=''
   exch=''
   code=''
   ltp=''
   open=''
   close=''
   high=''
   low=''

class PricekDOM:
   name=''
   rate=0
   close=0
   high=0
   low=0
   open=0
   average=0
   pivotpoint=0
   top_centre=0
   botom_centre=0
   time=''

class OrderDOM:
   name=''
   exch=''
   status=''
   order_id=''
   qty=''
   buy_sell_type=''

class SupportDOM:
   support=0
   resistance=0

class CEPENameDOM:
   ce_name=''
   pe_name=''

class StatusDOM:
   order_started=False
   chart_5min_placed=False
   chart_15min_placed=False
   ce_order_placed=False
   pe_order_placed=False
   ce_sell_order=False
   pe_sell_order=False
   ce_exit=False
   pe_exit=False

class CEPENamingRule:
   def get_cepe_name_shoonya(expiry_year,atm_strike,cepe_type):
      splist=expiry_year.split('-')
      mm_int=int(splist[1])
      abbr_month_name = calendar.month_abbr[mm_int]
      strDt=splist[2]+abbr_month_name.upper()+splist[0][-2:]
      #Find CE price NIFTY12JUN25C25200 
      if cepe_type=='CE':
         symbCE=f"NIFTY{strDt}C{atm_strike}"
      elif cepe_type=='PE':
         symbCE=f"NIFTY{strDt}P{atm_strike}"
      elif cepe_type=='1':
         symbCE=f"NIFTY{strDt}C{atm_strike}"
      elif cepe_type=='2':
         symbCE=f"NIFTY{strDt}P{atm_strike}"

      return symbCE
   
   def get_cepe_admin_shoonya(expiry_year,atm_strike,cepe_type):
      splist=expiry_year.split('-')
      strDt=splist[2]+splist[1].upper()+splist[0][-2:]
      #Find CE price NIFTY12JUN25C25200 
      if cepe_type=='CE':
         symbCE=f"NIFTY{strDt}C{atm_strike}"
      elif cepe_type=='PE':
         symbCE=f"NIFTY{strDt}P{atm_strike}"
      elif cepe_type=='1':
         symbCE=f"NIFTY{strDt}C{atm_strike}"
      elif cepe_type=='2':
         symbCE=f"NIFTY{strDt}P{atm_strike}"

      return symbCE
   