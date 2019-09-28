from math import cos, asin, sqrt

from means_of_transport.input.flash import get_flash_scooters
from means_of_transport.input.publi_bike import get_publi_bike_stations
from transport_type import TransportType


def get_personal_transport_list(user_lat, user_long):
    personal_transport_list = []
    personal_transport_list.extend(get_flash_scooters(user_long=user_long, user_lat=user_lat))
    personal_transport_list.extend(get_publi_bike_stations())
    return personal_transport_list


def get_personal_transport_output_list(user_lat, user_long):
    return list(map(lambda personal_transport: personal_transport.get_output_dict(),
                    get_personal_transport_list(user_lat=user_lat, user_long=user_long)))


def get_closest_personal_transports(user_lat, user_long):
    """
    Returns a list of closest available personal transports
    :param user_lat:
    :param user_long:
    :return:
    """
    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295  # Pi/180
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (
                1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))  # 2*R*asin...

    personal_transport_list = get_personal_transport_list(user_lat, user_long)
    # initialize dict with infinite distance value for each transport type
    closest_personal_transports = {transport_type: (None, float("inf")) for transport_type in
                                   TransportType}

    for personal_transport in personal_transport_list:
        abs_distance = abs(distance(user_lat, user_long,
                                    personal_transport.lat,
                                    personal_transport.long))
        _, current_min_distance = closest_personal_transports[personal_transport.type]
        if abs_distance < current_min_distance:
            closest_personal_transports[personal_transport.type] = (personal_transport, abs_distance)

    return [personal_transport for personal_transport, _ in closest_personal_transports.values() if
            personal_transport is not None]


if __name__ == '__main__':
    out = get_closest_personal_transports(47.3, 8.55)
    print(out)
    pass
