from api_helper import ShoonyaApiPy
import logging
import pyotp
 
#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()

#credentials
user    = 'FA189828'
pwd     = 'India@123'
factor2 = 'NUAW2A65Y6CLE767343R64H66V6342Q7'
vc      = 'FA189828_U'
app_key = '143c78338af58acd9002b781b621b7d1'
imei    = 'abc1234'

#make the api call
ret = api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(factor2).now(), vendor_code=vc, api_secret=app_key, imei=imei)

print(ret)

