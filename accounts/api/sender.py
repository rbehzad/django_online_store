import requests

def send_otp(otp):
    body = {'receptor':otp.receiver, 'token':otp.password, 'template': 'verify'}
    sms_res = requests.get('https://api.kavenegar.com/v1/6378704A6D784872707039496250775A48536F4A47786554694F377362315A357159492F4F6875506B4E453D/verify/lookup.json', params=body)
    
    print("otp password")
    print(otp.password)