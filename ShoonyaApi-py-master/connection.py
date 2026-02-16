from api_helper import ShoonyaApiPy
import yaml
import pyotp
import sound_data


class MyAPIConnection:
    def __init__(self):
        with open('cred.yml') as f:
         cred = yaml.load(f, Loader=yaml.FullLoader)
         self.api = ShoonyaApiPy()
         self.ret = self.api.login(userid = cred['user'], password = cred['pwd'], twoFA= pyotp.TOTP(cred['factor2']).now(), vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])
    def get_api_connection(self):
       return self.api

