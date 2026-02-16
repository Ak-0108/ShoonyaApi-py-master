from nsepython import *
import datetime
import dom_strike

def get_nifty_ltp():
 objBank=nse_fno("NIFTY")
 nifty_ltp=float(objBank["underlyingValue"])
 return nifty_ltp

def get_nifty_expiry():
 expValue=''
 lstExpiry=expiry_list('NIFTY')
 if len(lstExpiry)>0:
  expValue=str(lstExpiry[0])
 return expValue

def get_nifty_next_expiry():
 expValue=''
 lstExpiry=expiry_list('NIFTY')
 if len(lstExpiry)>0:
  expValue=str(lstExpiry[1])
 return expValue

def get_nifty_ce_strike():
 atm_ce= dom_strike.calculate_atm_strike(get_nifty_ltp())
 return atm_ce

def get_nifty_pe_strike():
 atm_pe= dom_strike.calculate_atm_put(get_nifty_ltp())
 return atm_pe

def get_nifty_ce_strike_by_rate(ltp):
 atm_ce= dom_strike.calculate_atm_strike(ltp)
 return atm_ce

def get_nifty_pe_strike_by_rate(ltp):
 atm_pe= dom_strike.calculate_atm_put(ltp)
 return atm_pe

def get_nifty_ce_ltp(ltp): 
 atm_ce= dom_strike.calculate_atm_strike(ltp)
 expiry_month=get_nifty_expiry()
 var_ce_info= nse_quote_ltp("NIFTY",expiry_month,"CE",atm_ce)
 return var_ce_info

def get_nifty_pe_ltp(ltp):
 atm_pe= dom_strike.calculate_atm_put(ltp)
 expiry_month=get_nifty_expiry()
 var_pe_info= nse_quote_ltp("NIFTY",expiry_month,"PE",atm_pe)
 return var_pe_info

#ICICI CE PE NAME
def get_Shoonya_ce_name(expiry_month,ltp): 
 var_ce_info= dom_strike.get_ce_name(expiry_month, ltp)
 return var_ce_info

def get_Shoonya_pe_name(expiry_month,ltp):
 var_pe_info=  dom_strike.get_pe_name(expiry_month, ltp)
 return var_pe_info

def get_ce_name_strike(expiry_month,strike_price): 
 var_ce_info= dom_strike.get_ce_name_strike(expiry_month, strike_price)
 return var_ce_info

def get_pe_name_strike(expiry_month,strike_price):
 var_pe_info=  dom_strike.get_pe_name_strike(expiry_month, strike_price)
 return var_pe_info


def get_nifty_ce_rate(atm_ce,expiry_month):
 var_pe_info=  nse_quote_ltp("NIFTY",expiry_month,"CE",atm_ce)
 return var_pe_info

def get_nifty_pe_rate(atm_pe,expiry_month):
 var_pe_info=  nse_quote_ltp("NIFTY",expiry_month,"PE",atm_pe)
 return var_pe_info

#Find CE price NIFTY12JUN25C25200 
#strDt=datetime.datetime.now().strftime("%d%b%y")
def calculate_cpr(high, low, close):
    """
    Calculates the Central Pivot Range (CPR) levels.

    Args:
      high: The previous day's high price.
      low: The previous day's low price.
      close: The previous day's closing price.

    Returns:
      A dictionary containing the Pivot Point, Bottom Central Pivot, and Top Central Pivot.
    """
    pivot_point = (high + low + close) / 3
    bottom_central_pivot = (high + low) / 2
    top_central_pivot = (pivot_point - bottom_central_pivot) + pivot_point
    return {
        "Pivot": pivot_point,
        "BottomCentralPivot": bottom_central_pivot,
        "TopCentralPivot": top_central_pivot,
    }


# Expected output: {'Pivot': 105.0, 'Bottom Central Pivot': 105.0, 'Top Central Pivot': 105.0}

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
        "PivotPoint": pivot_point,
        "Resistance1": r1,
        "Resistance2": r2,
        "Resistance3": r3,
        "Support1": s1,
        "Support2": s2,
        "Support3": s3,
    }

