from means_of_transport.personal_transport import PersonalTransport
from means_of_transport.input.flash import get_flash_scooters
from means_of_transport.input.publi_bike import get_publi_bike_stations


def get_personal_transport_list(user_long, user_lat):
    personal_transport_list = []
    personal_transport_list.extend(get_flash_scooters(user_long=user_long, user_lat=user_lat))
    personal_transport_list.extend(get_publi_bike_stations())
    return personal_transport_list


def get_personal_transport_output_list(user_long, user_lat):
    return list(map(lambda personal_transport: personal_transport.get_output_dict(),
                    get_personal_transport_list(user_long, user_lat)))


if __name__ == '__main__':
    out = get_personal_transport_output_list(8.55, 47.3)
    print(out)
    pass