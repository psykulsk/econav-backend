from directions_api.directions_api import get_google_route, NoGoogleRouteError, GOOGLE_TRAVEL_MODE_TO_TRANSPORT_TYPE
from means_of_transport.functions import get_closest_personal_transports
from transport_type import TransportType
from means_of_transport.personal_transport import PersonalTransport
from climate_api.carbon_footprint import TRANSPORT_TYPE_TO_CARBON_FOOTPRINT, get_transport_road_calc_5

TRANSPORT_TYPE_TO_GOOGLE_TRAVEL_MODE = {
    TransportType.BIKE: "bicycling",
    TransportType.E_BIKE: "bicycling",
    TransportType.E_CAR: "driving",
    TransportType.E_SCOOTER: "bicycling",
    TransportType.WALK: "walking",
    TransportType.MOTOR_SCOOTER: "driving"
}

TRANSPORT_TYPE_TO_CHF_PER_MINUTE = {
    TransportType.BIKE: 0.15,
    TransportType.E_BIKE: 0.25,
    TransportType.E_CAR: 0.88,
    TransportType.E_SCOOTER: 0.30,
    TransportType.WALK: 0.0,
    TransportType.MOTOR_SCOOTER: 0.35,
    TransportType.RAIL: 0.6,
    TransportType.METRO_RAIL: 0.6,
    TransportType.SUBWAY: 0.6,
    TransportType.TRAM: 0.6,
    TransportType.MONORAIL: 0.6,
    TransportType.HEAVY_RAIL: 0.6,
    TransportType.COMMUTER_TRAIN: 0.6,
    TransportType.HIGH_SPEED_TRAIN: 0.6,
    TransportType.LONG_DISTANCE_TRAIN: 0.6,
    TransportType.BUS: 0.6,
    TransportType.INTERCITY_BUS: 0.6,
    TransportType.TROLLEYBUS: 0.6,
    TransportType.SHARE_TAXI: 0.6,
    TransportType.FERRY: 0.6,
    TransportType.CABLE_CAR: 0.6,
    TransportType.GONDOLA_LIFT: 0.6,
    TransportType.FUNICULAR: 0.6,
    TransportType.OTHER: 0.6
}


def get_routes_for_transport_types(start_lat, start_long, end_lat, end_long):
    closest_personal_transports = get_closest_personal_transports(start_lat, start_long)
    personal_transport_full_route = []
    for personal_transport in closest_personal_transports:
        try:
            # First route walking from user position to vehicle
            walking_route = get_google_route(start_lat, start_long, personal_transport.lat, personal_transport.long,
                                             'walking')
            # Second route travel mode from vehicle position to end pos
            transport_route = get_google_route(personal_transport.lat, personal_transport.long, end_lat, end_long,
                                               TRANSPORT_TYPE_TO_GOOGLE_TRAVEL_MODE[personal_transport.type])
        except NoGoogleRouteError:
            continue
        walking_route_distance = walking_route.get('distance', {}).get('value')
        walking_route_time_sec = walking_route.get('duration', {}).get('value')

        transport_route_distance_meters = transport_route.get('distance', {}).get('value')
        transport_route_time_sec = transport_route.get('duration', {}).get('value')
        transport_route_footprint_kg = transport_route_distance_meters * TRANSPORT_TYPE_TO_CARBON_FOOTPRINT.get(
            personal_transport.type, 0.0)
        transport_route_cost = (transport_route_time_sec / 60.0) * TRANSPORT_TYPE_TO_CHF_PER_MINUTE.get(
            personal_transport.type)

        walking_route_data = {
            'personal_transport': PersonalTransport(TransportType.WALK, 'walk', start_lat,
                                                    start_long).get_output_dict(),
            'route': walking_route.get('steps'),
            'cost': 0.0,
            'carbon_footprint': 0.0,
            'time': walking_route_time_sec
        }
        transport_route_data = {
            'personal_transport': personal_transport.get_output_dict(),
            'route': transport_route.get('steps'),
            'cost': transport_route_cost,
            'carbon_footprint': transport_route_footprint_kg,
            'time': walking_route_time_sec
        }
        gas_carbon_footprint = get_transport_road_calc_5(3000, (
                transport_route_distance_meters + walking_route_distance) / 1000.0)

        personal_transport_data = {
            'carbon_footprint': transport_route_footprint_kg,
            'gas_car_carbon_footprint': gas_carbon_footprint,
            'total_time': transport_route_time_sec + walking_route_time_sec,
            'total_cost': transport_route_cost,
            'routes': [
                walking_route_data, transport_route_data
            ]
        }
        personal_transport_full_route.append(personal_transport_data)

    # TODO add get_public_transport_route
    public_routes_list = get_public_transport_route(start_lat, start_long, end_lat, end_long)
    personal_transport_full_route.extend(public_routes_list)
    return personal_transport_full_route


def get_public_transport_route(start_lat, start_long, end_lat, end_long):
    try:
        transit_route = get_google_route(start_lat, start_long, end_lat, end_long,
                                         'transit')
    except NoGoogleRouteError:
        return []

    public_transport_routes = []
    total_carbon_footprint = 0.0
    total_cost = 0.0
    total_time = transit_route.get('duration').get('value')
    total_distance = transit_route.get('distance').get('value')
    for step in transit_route.get('steps'):
        if step.get('travel_mode') == 'WALKING':
            type = TransportType.WALK
            company = 'walk'
            route = step.get('steps')
        else:
            vehicle_type = step.get('transit_details').get('line').get('vehicle').get('type')
            type = GOOGLE_TRAVEL_MODE_TO_TRANSPORT_TYPE[vehicle_type]
            company = 'city'
            route = [step]
        start_location = step.get('start_location')
        distance = step.get('distance').get('value')
        duration = step.get('duration').get('value')
        cost = duration / 60 * TRANSPORT_TYPE_TO_CHF_PER_MINUTE[type]
        carbon_footprint = TRANSPORT_TYPE_TO_CARBON_FOOTPRINT[type] * distance
        route_data = {
            'personal_transport': PersonalTransport(type, company, start_location.get('lat'),
                                                    start_location.get('lng')).get_output_dict(),
            'route': route,
            'cost': cost,
            'carbon_footprint': carbon_footprint,
            'time': duration
        }
        public_transport_routes.append(route_data)
        total_carbon_footprint += carbon_footprint
        total_cost += cost

    gas_carbon_footprint = get_transport_road_calc_5(3000, total_distance / 1000.0)
    personal_transport_data = {
        'carbon_footprint': total_carbon_footprint,
        'gas_car_carbon_footprint': gas_carbon_footprint,
        'total_time': total_time,
        'total_cost': total_cost,
        'routes': public_transport_routes

    }
    return [personal_transport_data]


if __name__ == '__main__':
    routes = get_routes_for_transport_types(47.3, 8.51, 47.4, 8.49)
    # routes = get_public_transport_route(47.3, 8.51, 47.35, 8.503)
    pass
