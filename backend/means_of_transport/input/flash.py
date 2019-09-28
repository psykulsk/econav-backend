import requests
import json
import logging

from backend.means_of_transport.personal_transport import PersonalTransport

FLASH_GET_ENDPOINT = 'https://api.goflash.com/api/Mobile/Scooters'


def flash_scooter_to_personal_transport(flash_scooter_response_data):
    type = 'scooter'
    company = 'flash'
    long = flash_scooter_response_data["location"]["longitude"]
    lat = flash_scooter_response_data["location"]["latitude"]
    return PersonalTransport(type=type, company=company, long=long, lat=lat)


def get_flash_scooters(user_long, user_lat):
    response = requests.get(FLASH_GET_ENDPOINT, params={
        'userLatitude': user_lat,
        'userLongitude': user_long,
        'lang': 'de',
        'latitude': user_lat,
        'longitude': user_long,
        'latitudeDelta': 0.1,
        'longitudeDelta': 0.1
    })
    if response.status_code != 200:
        logging.error('Flush get scooters request returned {0}'.format(response.status_code))
        return []
    else:
        response_json = json.loads(response.text)
        flash_scooters_response_list = response_json['Data']['Scooters']
        personal_transport_list = []
        for flash_scooter_response_data in flash_scooters_response_list:
            personal_transport_list.append(
                flash_scooter_to_personal_transport(flash_scooter_response_data)
            )
        return personal_transport_list
