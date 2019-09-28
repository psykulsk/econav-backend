import requests
import json
import logging
from transport_type import TransportType

CLIMATE_PARTNER_CALC_ENDPOINT = "https://climate-api-test.dakar.moccu.net/api/calculate"
API_KEY = "2947ee2d-bca1-4bc4-aa81-017ca40cb5b3"
HEADER = {'X-Api-Key': API_KEY}

TRANSPORT_TYPE_TO_VEHICLE_TYPE = {
    TransportType.BIKE: "normal_bike",
    TransportType.E_BIKE: "e-bike",
    TransportType.E_CAR: "electric_car",
    TransportType.E_SCOOTER: "electric_scooter",
    TransportType.WALK: "walk",
    TransportType.MOTOR_SCOOTER: "motor_scooter",
}

# in kg per meter
TRANSPORT_TYPE_TO_CARBON_FOOTPRINT = {
    TransportType.BIKE: 0.000021,
    TransportType.E_BIKE: 0.000022,
    TransportType.E_CAR: 0.000043,
    TransportType.E_SCOOTER: 0.000025,
    TransportType.WALK: 0.0,
    TransportType.MOTOR_SCOOTER: 0.00008,
    TransportType.RAIL: 0.00010,
    TransportType.METRO_RAIL: 0.00010,
    TransportType.SUBWAY: 0.00010,
    TransportType.TRAM: 0.00010,
    TransportType.MONORAIL: 0.00010,
    TransportType.HEAVY_RAIL: 0.00010,
    TransportType.COMMUTER_TRAIN: 0.00010,
    TransportType.HIGH_SPEED_TRAIN: 0.00010,
    TransportType.LONG_DISTANCE_TRAIN: 0.00010,
    TransportType.BUS: 0.00010,
    TransportType.INTERCITY_BUS: 0.00010,
    TransportType.TROLLEYBUS: 0.00010,
    TransportType.SHARE_TAXI: 0.00010,
    TransportType.FERRY: 0.00010,
    TransportType.CABLE_CAR: 0.00010,
    TransportType.GONDOLA_LIFT: 0.00010,
    TransportType.FUNICULAR: 0.00010,
    TransportType.OTHER: 0.00010
}


def check_max(val, max, descr):
    if val > max:
        logging.warning(f"val={val} greater than max={max} for {descr}. Using max for query")
        return max
    return val


def extract_result(response: requests.Response):
    if response.status_code != 200:
        logging.error(f"get_zurich_vehicle_type_calc returned {response.status_code}")
        return None
    else:
        response_json = json.loads(response.text)
        return response_json["result"]


def get_transport_road_calc_5(weight_kg: float, distance_km: float):
    MAX_WEIGHT = 1000000000
    MAX_DISTANCE = 1000000000

    weight_kg = check_max(weight_kg, MAX_WEIGHT, "weight_kg")
    distance_km = check_max(distance_km, MAX_DISTANCE, "distance_km")

    data = {
        "calculation":
            {
                "type": "transport-road-calculation-5",
                "weight_kg": weight_kg,
                "distance_km": distance_km
            }
    }
    response = requests.post(url=CLIMATE_PARTNER_CALC_ENDPOINT, json=data, headers=HEADER)
    return extract_result(response)


def get_transport_air_calc_3(weight_kg: float, distance_km: float):
    MAX_WEIGHT = 1000000000
    MAX_DISTANCE = 1000000000

    weight_kg = check_max(weight_kg, MAX_WEIGHT, "weight_kg")
    distance_km = check_max(distance_km, MAX_DISTANCE, "distance_km")

    data = {
        "calculation":
             {
                "type": "transport-air-calculation-3",
                "weight_kg": weight_kg,
                "distance_km": distance_km
            }
    }
    response = requests.post(url=CLIMATE_PARTNER_CALC_ENDPOINT, json=data, headers=HEADER)
    return extract_result(response)


def get_zurich_vehicle_type_calc_9(transport_type: TransportType, distance_km: float):
    MAX_DISTANCE_KM = 1000000.0
    if distance_km > MAX_DISTANCE_KM:
        logging.warning(f"distance_km={distance_km} greater than MAX_DISTANCE_KM={MAX_DISTANCE_KM}. "
                        f"Querying for max value")
        distance_km = MAX_DISTANCE_KM

    data = {"calculation":
        {
            "type": "zurich_vehicle_type-calculation-9",
            "vehicle_type": TRANSPORT_TYPE_TO_VEHICLE_TYPE[transport_type],
            "kilometers": distance_km
        }
    }
    response = requests.post(url=CLIMATE_PARTNER_CALC_ENDPOINT, json=data, headers=HEADER)
    return extract_result(response)


if __name__ == "__main__":
    result_road_calc_5 = get_transport_road_calc_5(1000.0, 1000.0)
    result_air_calc_3 = get_transport_air_calc_3(1000, 1000)
    zurich_vehicle_type_calc_9 = get_zurich_vehicle_type_calc_9(TransportType.BIKE, 10.0)

    print(f"result_road_calc_5={result_road_calc_5}")
    print(f"result_air_calc_3={result_air_calc_3}")
    print(f"zurich_vehicle_type_calc_9={zurich_vehicle_type_calc_9}")