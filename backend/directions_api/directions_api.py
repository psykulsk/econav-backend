import googlemaps
import os
import logging
from datetime import datetime

gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_DIRECTIONS_API_KEY'))


def get_google_route(start_lat, start_long, end_lat, end_long, travel_mode):
    now = datetime.now()
    directions_result = gmaps.directions("{0},{1}".format(start_lat, start_long),
                                         "{0},{1}".format(end_lat, end_long),
                                         mode=travel_mode)
    # First leg is the first route proposed by google (sometimes google can return a few legs,
    # with alternative routes. We always pick the first one for simplicity

    try:
        first_leg = directions_result[0].get('legs')[0]
    except (KeyError, IndexError):
        logging.error("No routes returned")
        return {}
    return first_leg


if __name__ == '__main__':
    leg = get_google_route(47.3, 8.51, 47.35, 8.503, 'walking')
    pass
