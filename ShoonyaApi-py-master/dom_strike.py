import math
from nsepython import *

def calculate_atm_strike(nifty_ltp):
    strike_increment=100
       # Round down to the nearest increment
    val1 = math.floor(nifty_ltp / strike_increment) * strike_increment

       # Round up to the nearest increment
    val2 = math.ceil(nifty_ltp / strike_increment) * strike_increment

       # Return the closest value to the Nifty LTP
    temp_var= val1 if abs(nifty_ltp - val1) > abs(nifty_ltp - val2) else val2
    return temp_var+100

def calculate_atm_put(nifty_ltp):
    strike_increment=100
       # Round down to the nearest increment
    val1 = math.floor(nifty_ltp / strike_increment) * strike_increment

       # Round up to the nearest increment
    val2 = math.ceil(nifty_ltp / strike_increment) * strike_increment

       # Return the closest value to the Nifty LTP
    temp_var= val1 if abs(nifty_ltp - val1) < abs(nifty_ltp - val2) else val2
    return temp_var-100

def get_current_expiry():
   expValue=''
   lstExpiry=expiry_list('NIFTY')
   if len(lstExpiry)>0:
    expValue=str(lstExpiry[0])
   return expValue

def get_next_expiry():
   expValue=''
   lstExpiry=expiry_list('NIFTY')
   if len(lstExpiry)>1:
    expValue=str(lstExpiry[1])
   return expValue

def get_ce_name(expiry_year,nifty_ltp):
 splist=expiry_year.split('-')
 strDt=splist[0]+splist[1].upper()+splist[2][-2:]
 atm_strike= calculate_atm_strike(float(nifty_ltp))
 #Find CE price NIFTY12JUN25C25200 
 symbCE=f"NIFTY{strDt}C{atm_strike}"
 return symbCE

def get_pe_name(expiry_year,nifty_ltp):
 splist=expiry_year.split('-')
 strDt=splist[0]+splist[1].upper()+splist[2][-2:]
 atm_strike= calculate_atm_put(float(nifty_ltp))
 #Find CE price NIFTY12JUN25C25200 
 symbCE=f"NIFTY{strDt}P{atm_strike}"
 return symbCE

def get_ce_name_strike(expiry_year,atm_strike):
 splist=expiry_year.split('-')
 strDt=splist[0]+splist[1].upper()+splist[2][-2:]
 #Find CE price NIFTY12JUN25C25200 
 symbCE=f"NIFTY{strDt}C{atm_strike}"
 return symbCE

def get_pe_name_strike(expiry_year,atm_strike):
 splist=expiry_year.split('-')
 strDt=splist[0]+splist[1].upper()+splist[2][-2:]
 #Find CE price NIFTY12JUN25C25200 
 symbCE=f"NIFTY{strDt}P{atm_strike}"
 return symbCE

def get_ce_name_nextweek(nifty_ltp):
 expiry_year=get_next_expiry()
 splist=expiry_year.split('-')
 strDt=splist[0]+splist[1]+splist[2][-2:]
 atm_strike= calculate_atm_strike(nifty_ltp)
 #Find CE price NIFTY12JUN25C25200 
 symbCE=f"NIFTY{strDt}C{atm_strike}"
 return symbCE

def get_pe_name_nextweek(nifty_ltp):
 expiry_year=get_next_expiry()
 splist=expiry_year.split('-')
 strDt=splist[0]+splist[1]+splist[2][-2:]
 atm_strike= calculate_atm_put(nifty_ltp)
 #Find CE price NIFTY12JUN25C25200 
 symbCE=f"NIFTY{strDt}P{atm_strike}"
 return symbCE

#Below are used by nsepy
def get_nifty_ltp():
 objBank=nse_fno("NIFTY")
 nifty_ltp=float(objBank["underlyingValue"])
 return nifty_ltp

def get_nifty_ce_rate(atm_ce,expiry_month):
 var_pe_info=  nse_quote_ltp("NIFTY",expiry_month,"CE",atm_ce)
 return var_pe_info

def get_nifty_pe_rate(atm_pe,expiry_month):
 var_pe_info=  nse_quote_ltp("NIFTY",expiry_month,"PE",atm_pe)
 return var_pe_info

def calculate_pivot_points(high, low, close):
    """
    Calculates classic pivot points, including support and resistance levels.

    Args:
        high (float): The previous day's high price.
        low (float): The previous day's low price.
        close (float): The previous day's closing price.

    Returns:
        dict: A dictionary containing the calculated pivot point, support levels,
              and resistance levels.
    """
    pivot_point = (high + low + close) / 3

    # Resistance levels
    r1 = (2 * pivot_point) - low
    r2 = pivot_point + (high - low)
    r3 = high + 2 * (pivot_point - low)

    # Support levels
    s1 = (2 * pivot_point) - high
    s2 = pivot_point - (high - low)
    s3 = low - 2 * (high - pivot_point)

    return {
        "Pivot Point": pivot_point,
        "Resistance 1 (R1)": r1,
        "Resistance 2 (R2)": r2,
        "Resistance 3 (R3)": r3,
        "Support 1 (S1)": s1,
        "Support 2 (S2)": s2,
        "Support 3 (S3)": s3,
    }

#previous day high,low & closing price
def calculate_pcr(high,low,close):
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (pivot - bc) + pivot

    return {
        "PivotPoint": pivot,
        "BC": bc,
        "TC": tc,
     }
 