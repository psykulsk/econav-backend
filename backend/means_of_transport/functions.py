from math import cos, asin, sqrt

from means_of_transport.input.flash import get_flash_scooters
from means_of_transport.input.publi_bike import get_publi_bike_stations
from means_of_transport.input.bird import get_bird_from_dump
from means_of_transport.input.mobility_mock import read_mobility_motor_scooters
from transport_type import TransportType


def get_personal_transport_list(user_lat, user_long):
    """
    Returns list of all available personal transports returned by APIs
    :param user_lat:
    :param user_long:
    :return: list of PersonalTransport objects representing different means of personal transport.
    """
    personal_transport_list = []
    personal_transport_list.extend(get_flash_scooters(user_long=user_long, user_lat=user_lat))
    personal_transport_list.extend(get_publi_bike_stations())
    personal_transport_list.extend(get_bird_from_dump())
    personal_transport_list.extend(read_mobility_motor_scooters())
    return personal_transport_list


def get_filtered_personal_transport_list(user_lat, user_long, radius):
    """
    Returns a list of PublicTransport objects which are within the given radius from the user.
    :param user_lat:
    :param user_long:
    :param radius:
    :return:
    """
    personal_transport_list = get_personal_transport_list(user_lat, user_long)
    filtered_list = []
    for pt in personal_transport_list:
        pt_lat = pt.lat
        pt_long = pt.long
        if distance(user_lat, user_long, pt_lat, pt_long) <= radius:
            filtered_list.append(pt)
    return filtered_list


def get_filtered_personal_transport_output_list(user_lat, user_long, radius):
    """
    Returns a list of python dictionaries representing various means of personal transport.
    :param user_lat:
    :param user_long:
    :param radius:
    :return:
    """
    return list(map(lambda personal_transport: personal_transport.get_output_dict(),
                    get_filtered_personal_transport_list(user_lat=user_lat, user_long=user_long, radius=radius)))


def get_closest_personal_transports(user_lat, user_long, dest_lat, dest_long):
    """
    Returns a list of closest available personal transports
    :param user_lat:
    :param user_long:
    :param dest_lat:
    :param dest_long:
    :return:
    """
    personal_transport_list = get_personal_transport_list(user_lat, user_long)
    # initialize dict with infinite distance value for each transport type
    closest_personal_transports = {transport_type: (None, float("inf")) for transport_type in
                                   TransportType}

    for personal_transport in personal_transport_list:
        abs_distance_from_vehicle_to_dest = abs(distance(dest_lat, dest_long,
                                                         personal_transport.lat,
                                                         personal_transport.long))
        if personal_transport.remaining_range is not None:
            if abs_distance_from_vehicle_to_dest > personal_transport.remaining_range:
                continue
        abs_distance = abs(distance(user_lat, user_long,
                                    personal_transport.lat,
                                    personal_transport.long))
        _, current_min_distance = closest_personal_transports[personal_transport.type]
        if abs_distance < current_min_distance:
            closest_personal_transports[personal_transport.type] = (personal_transport, abs_distance)

    return [personal_transport for personal_transport, _ in closest_personal_transports.values() if
            personal_transport is not None]


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (
            1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin...


if __name__ == '__main__':
    hack_zurich_lat = 47.390229
    hack_zurich_long = 8.514694
    personal_transport = get_personal_transport_list(hack_zurich_lat, hack_zurich_long)
    print(personal_transport)
    closest_personal_transport = get_closest_personal_transports(hack_zurich_lat, hack_zurich_long)
    print(closest_personal_transport)
    pass
