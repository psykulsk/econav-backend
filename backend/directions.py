from directions_api.directions_api import get_google_route
from means_of_transport.functions import get_closest_personal_transports
from transport_type import TransportType
from means_of_transport.personal_transport import PersonalTransport

TRANSPORT_TYPE_TO_GOOGLE_TRAVEL_MODE = {
    TransportType.BIKE: "bicycling",
    TransportType.E_BIKE: "bicycling",
    TransportType.E_CAR: "driving",
    TransportType.E_SCOOTER: "bicycling",
    TransportType.WALK: "walking",
    TransportType.MOTOR_SCOOTER: "motor_scooter"
}


def get_routes_for_transport_types(start_lat, start_long, end_lat, end_long):
    closest_personal_transports = get_closest_personal_transports(start_lat, start_long)
    personal_transport_full_route = []
    for personal_transport in closest_personal_transports:
        # First route walking from user position to vehicle
        walking_route = get_google_route(start_lat, start_long, personal_transport.lat, personal_transport.long,
                                         'walking')
        # Second route travel mode from vehicle position to end pos
        transport_route = get_google_route(personal_transport.lat, personal_transport.long, end_lat, end_long,
                                           TRANSPORT_TYPE_TO_GOOGLE_TRAVEL_MODE[personal_transport.type])
        walking_route_data = {
            'personal_transport': PersonalTransport(TransportType.WALK, 'null', start_lat,
                                                    start_long).get_output_dict(),
            'route': walking_route.get('steps')
        }
        transport_route_data = {
            'personal_transport': personal_transport.get_output_dict(),
            'route': transport_route.get('steps')
        }
        personal_transport_data = {
            'carbon_footprint': 1.0,  # TODO use climate_api for this val
            'gas_carbon_footprint': 10.0,  # TODO
            'total_time': 1.0,
            'total_cost': 1.0,  # TODO mock costs
            'routes': [
                walking_route_data, transport_route_data
            ]
        }
        personal_transport_full_route.append(personal_transport_data)

    # TODO add get_public_transport_route
    return personal_transport_full_route


def get_public_transport_route(start_lat, start_long, end_lat, end_long):
    pass


if __name__ == '__main__':
    routes = get_routes_for_transport_types(47.3, 8.51, 47.35, 8.503)
    pass
