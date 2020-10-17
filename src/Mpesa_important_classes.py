from datetime import datetime
import keys
import base64
import requests
from requests.auth import HTTPBasicAuth

class DateFormated:
    unformated_time = datetime.now()
    formated_time = unformated_time.strftime("%Y%m%d%H%M%S")
    
class Base64Pass:
    data_to_encode = keys.BusinessShortCode + keys.lipa_na_mpesa_passkey + DateFormated.formated_time
    encoded_string = base64.b64encode(data_to_encode.encode())
    decoded_password =  encoded_string.decode('utf-8')
    
class AccessToken:
    def __init__(self,consumer_key,consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
    def access_token(self):
        consumer_key = self.consumer_key
        consumer_secret = self.consumer_secret
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        json_reponse = r.json()
        accetoken = json_reponse["access_token"]
        return accetoken

class LipaNaMpesa:
    def __init__(self,phoneNumber,accountReference,amount):
        self.phoneNumber = phoneNumber
        self.accountReference = accountReference
        self.amount = amount
        
        
    def lipa_na_mpesa(self):
        access_token_class = AccessToken(keys.Consumer_key,keys.Consumer_secret)
        access_token = access_token_class.access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
        "BusinessShortCode": keys.BusinessShortCode,
        "Password": Base64Pass.decoded_password,
        "Timestamp": DateFormated.formated_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(self.amount),
        "PartyA": str(self.phoneNumber),
        "PartyB": keys.BusinessShortCode,
        "PhoneNumber": str(self.phoneNumber),
        "CallBackURL": "https://fullstack.com/callback",
        "AccountReference": str(self.accountReference),
        "TransactionDesc": "Twala Fish order transaction"
        }
        
        response = requests.post(api_url, json = request, headers=headers)

        return response.text
    

lipa_na_mpesa = LipaNaMpesa(254704157038,33380005,1)
print(lipa_na_mpesa.lipa_na_mpesa())
        
        
        
        