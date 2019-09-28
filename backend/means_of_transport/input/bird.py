import requests
import json
import logging
import uuid
import os

from means_of_transport.transport_type_mapping import TRANSPORT_TYPE_TO_OUTPUT_TYPE
from transport_type import TransportType
from means_of_transport.personal_transport import PersonalTransport

LOGIN_ENDPOINT = "https://api.birdapp.com/user/login"
GUID = uuid.uuid4()
APP_VERSION='4.41.0'
LOGIN_HEADERS = {'User-Agent': 'Bird/4.41.0 (co.bird.Ride; build:37; iOS 12.3.1) Alamofire/4.41.0',
           'Device-Id': str(GUID),
           'Platform': 'android',
           'App-Version': str(APP_VERSION),
           'Content-Type': 'application/json'}

BIRD_ID = '599056be-c517-4991-b8ef-8be4e05ef0e4'
BIRD_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6Ijg4ZTk5NDgxLTZlODAtNGU1My1iN2E2LWVkNDQ0YTA2N2E2YSIs" \
           "ImRldmljZV9pZCI6IjUzMjJjZTljLTc3ODMtNDM5Yy1iNTZhLTFmY2IxY2QyMjFmZiIsImV4cCI6MTYwMTE5NzI1N30.0_6rQJJRC1SQf" \
           "AT8UNcWmG8HTlXex2QPz7PGkco_kWI"

EMAIL = "jakub.golinowski@gmail.com"

GEO_ENDPOINT = "https://api.birdapp.com/bird/nearby"

SEARCH_RADIUS = 1000



BACKEND_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIRD_DUMP_PATH = os.path.join(BACKEND_BASE_DIR, "data", "bird.json")



def renew_id():
    global BIRD_ID
    body = {"email": EMAIL}

    r = requests.post(url=LOGIN_ENDPOINT, json=body, headers=LOGIN_HEADERS)
    print(r.text)
    response_json = json.loads(r.text)
    BIRD_ID = response_json["id"]


# We want to renew ID once per request so we put it here in the global code
# Not running the renew on the server -> no permission


def bird_scooter_to_personal_transport(bird_scooter):
    type = TransportType.E_SCOOTER
    company = 'bird'
    try:
        lat = bird_scooter["location"]["latitude"]
        long = bird_scooter["location"]["longitude"]
        remaining_range_int = float(bird_scooter["estimated_range"])/1000.0
    except(KeyError, ValueError, TypeError) as err:
        return None

    return PersonalTransport(type=type, company=company, long=long, lat=lat, remaining_range=remaining_range_int)


def get_bird_scooters_from_api(user_lat, user_long):
    renew_id()
    location_dict = {
        "latitude": user_lat,
        "longitude": user_long,
        "altitude": 500,
        "accuracy": 100,
        "speed": -1,
        "heading": -1
    }

    params_dict = {
        "latitude": str(user_lat),
        "longitude": str(user_long),
        "radius": str(SEARCH_RADIUS)
    }

    location_json = json.dumps(location_dict)

    # Authorization: Bird <TOKEN> – Use the token you got from Auth-Request.
    # Device-id: <GUID> – You can reuse the GUID from Auth-Request, but don't have to
    # App-Version: 4.41.0
    # Location: {"latitude":37.77249,"longitude":-122.40910,"altitude":500,"accuracy":100,"speed":-1,"heading":-1}
    # – Yes this is JSON in a header ;) – You should use the same data like from the GET request params.
    geo_headers = {
        "Authorization": "Bird " + str(BIRD_TOKEN),
        "Devide-id": str(GUID),
        "App-Version": str(APP_VERSION),
        "Location": str(location_json),
    }
    response = requests.get(url=GEO_ENDPOINT, headers=geo_headers, params=params_dict)

    if response.status_code != 200:
        logging.error('BIRD get scooters request returned {0}'.format(response.status_code))
        return []
    else:
        response_json = json.loads(response.text)
        dump_bird(response_json)
        return convert_response_to_personal_transport_list(response_json)


def convert_response_to_personal_transport_list(response_json):
    bird_scooter_list = response_json.get('birds', {})
    personal_transport_list = []
    for bird_scooter in bird_scooter_list:
        pt = bird_scooter_to_personal_transport(bird_scooter)
        if pt is not None:
            personal_transport_list.append(pt)
    return personal_transport_list


def get_bird_from_dump():
    historic_response_json = load_bird()
    return convert_response_to_personal_transport_list(historic_response_json)


def dump_bird(api_response_json):
    with open(BIRD_DUMP_PATH, 'w') as bird_dump:
        json.dump(api_response_json, bird_dump)


def load_bird():
    with open(BIRD_DUMP_PATH) as bird_dump:
        return json.load(bird_dump)


if __name__ == "__main__":
    hack_zurich_lat = 47.390229
    hack_zurich_long = 8.514694
    # bird_scooters = get_bird_scooters_from_api(hack_zurich_lat, hack_zurich_long)
    # print(bird_scooters)
    bird_scooters_dump = get_bird_from_dump()
    print(bird_scooters_dump)
