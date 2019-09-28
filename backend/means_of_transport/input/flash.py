import requests
import json
import logging

from transport_type import TransportType
from means_of_transport.personal_transport import PersonalTransport

FLASH_GET_ENDPOINT = 'https://api.goflash.com/api/Mobile/Scooters'


def flash_scooter_to_personal_transport(flash_scooter_response_data):
    type = TransportType.E_SCOOTER
    company = 'flash'
    try:
        lat = flash_scooter_response_data["location"]["latitude"]
        long = flash_scooter_response_data["location"]["longitude"]
        remainder_range = flash_scooter_response_data["RemainderRange"]
    except (KeyError,TypeError) as err:
        return None

    try:
        remainder_range_km = float(remainder_range.strip(" km"))
    except ValueError as err:
        return None
    return PersonalTransport(type=type, company=company, long=long, lat=lat, remaining_range=remainder_range_km)


def get_flash_scooters(user_lat, user_long):
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
            pt = flash_scooter_to_personal_transport(flash_scooter_response_data)
            if pt is not None:
                personal_transport_list.append(pt)
        return personal_transport_list


if __name__ == "__main__":
    hack_zurich_lat = 47.390229
    hack_zurich_long = 8.514694

    flash_scooters = get_flash_scooters(hack_zurich_lat, hack_zurich_long)
    print(flash_scooters)