from api_helper import ShoonyaApiPy
import yaml
import pyotp

#yaml for parameters
with open('cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    
    print("User: "+cred['user'])
    print("Password: "+cred['pwd'])
    inputvalue=input("Press 1 to generate OTP\n")
    if inputvalue.lower()=='1':
        otpStr=pyotp.TOTP(cred['factor2']).now()
        print("OTP is Below:\n")
        print(otpStr)
        print("\n")
        iv=input("Press 2 to Refresh OTP:")
        if iv=='2':
            otpStr=pyotp.TOTP(cred['factor2']).now()
            print(otpStr)

