import os
import googlemaps
from transport_type import TransportType

gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_DIRECTIONS_API_KEY'))


class NoGoogleRouteError(Exception):
    pass


GOOGLE_TRAVEL_MODE_TO_TRANSPORT_TYPE = {
    "RAIL": TransportType.RAIL,
    "METRO_RAIL": TransportType.METRO_RAIL,
    "SUBWAY": TransportType.SUBWAY,
    "TRAM": TransportType.TRAM,
    "MONORAIL": TransportType.MONORAIL,
    "HEAVY_RAIL": TransportType.HEAVY_RAIL,
    "COMMUTER_TRAIN": TransportType.COMMUTER_TRAIN,
    "HIGH_SPEED_TRAIN": TransportType.HIGH_SPEED_TRAIN,
    "LONG_DISTANCE_TRAIN": TransportType.LONG_DISTANCE_TRAIN,
    "BUS": TransportType.BUS,
    "INTERCITY_BUS": TransportType.INTERCITY_BUS,
    "TROLLEYBUS": TransportType.TROLLEYBUS,
    "SHARE_TAXI": TransportType.SHARE_TAXI,
    "FERRY": TransportType.FERRY,
    "CABLE_CAR": TransportType.CABLE_CAR,
    "GONDOLA_LIFT": TransportType.GONDOLA_LIFT,
    "FUNICULAR": TransportType.FUNICULAR,
    "OTHER": TransportType.OTHER
}


def get_google_route(start_lat, start_long, end_lat, end_long, travel_mode):
    directions_result = gmaps.directions("{0},{1}".format(start_lat, start_long),
                                         "{0},{1}".format(end_lat, end_long),
                                         mode=travel_mode)
    # First leg is the first route proposed by google (sometimes google can return a few legs,
    # with alternative routes. We always pick the first one for simplicity

    if len(directions_result) == 0:
        raise NoGoogleRouteError
    first_leg = directions_result[0].get('legs')[0]
    return first_leg


if __name__ == '__main__':
    leg = get_google_route(47.3, 8.51, 0.0, 0.0, 'transit')
    pass
