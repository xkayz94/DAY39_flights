import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

SHEETY_ENDPOINT = 'https://api.sheety.co/5aeed4839c8f9f87c122bf9ed59a8a3d/flightDeals/prices'

load_dotenv()





class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.user = os.environ['USERNAME_SHEETY']
        self.password = os.environ['PASSWORD_SHEETY']
        self.authorization = HTTPBasicAuth(self.user, self.password)



    def get_destination(self):
        response = requests.get(url=SHEETY_ENDPOINT, auth=self.authorization)
        data = response.json()
        self.destination_data = data['prices']

        return self.destination_data


    def update_destination(self):
        for code in self.destination_data:
            parameter_code = {
                'price': {
                    'iataCode': code['iataCode']
                }
            }

            response_iata = requests.put(url=f'{SHEETY_ENDPOINT}/{code['id']}', json=parameter_code, auth=self.authorization)
            print(response_iata.text)




