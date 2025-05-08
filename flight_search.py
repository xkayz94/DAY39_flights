import requests
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

TOKEN_ENDPOINT = 'https://test.api.amadeus.com/v1/security/oauth2/token'
IATA_ENDPOINT = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
FLIGHT_ENDPOINT = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
today = datetime.today()
formatted_date = today.strftime("%Y-%m-%d")


class FlightSearch:


    def __init__(self):
        self.api_key = os.environ['API_KEY_AMADEUS']
        self.secret_key = os.environ['API_SECRET_AMADEUS']
        self.token = self.get_new_token()


    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key,
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)

        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        # code = 'TESTING'
        # return code
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        query = {
            'keyword': city_name,
            'max': 2,
            'include': 'AIRPORTS'
        }

        response = requests.get(url=IATA_ENDPOINT, params=query, headers=headers)


        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        query = {
            'originLocationCode': origin_city_code,
            'destinationLocationCode': destination_city_code,
            'departureDate': from_time.strftime("%Y-%m-%d"),
            'returnDate': to_time.strftime("%Y-%m-%d"),
            'adults': 1,
            'nonStop': 'true',
            'currencyCode': 'GBP',
            'max': 10,

        }

        response = requests.get(url=FLIGHT_ENDPOINT, params=query, headers=headers)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()