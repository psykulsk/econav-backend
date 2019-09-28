import requests
import json
import logging

from means_of_transport.personal_transport import PersonalTransport
from means_of_transport.transport_type_mapping import TRANSPORT_TYPE_TO_OUTPUT_TYPE
from transport_type import TransportType

PUBLI_BIKE_GET_ENDPOINT = \
    'https://data.stadt-zuerich.ch/dataset/d8951db3-4df1-483d-af1e-b34211c63ee9/resource/' \
    '91d89d8b-bfb4-4ca0-a2dd-3dbce11817c4/download/publibike.json'


def publi_bike_to_personal_transport(publi_bike_station):
    type = TransportType.BIKE
    company = 'publi_bike'
    long = publi_bike_station["geometry"]["coordinates"][0]
    lat = publi_bike_station["geometry"]["coordinates"][1]
    return PersonalTransport(type=type, company=company, long=long, lat=lat)


def get_publi_bike_stations():
    response = requests.get(PUBLI_BIKE_GET_ENDPOINT)
    if response.status_code != 200:
        logging.error('Flush get scooters request returned {0}'.format(response.status_code))
        return []
    else:
        response_json = json.loads(response.text)
        publi_bike_response_stations = response_json['features']
        personal_transport_list = []
        for publi_bike_station in publi_bike_response_stations:
            personal_transport_list.append(
                publi_bike_to_personal_transport(publi_bike_station)
            )
        return personal_transport_list


if __name__ == "__main__":
    publi_bike_list = get_publi_bike_stations()
    print(publi_bike_list)
