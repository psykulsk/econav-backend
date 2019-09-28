import requests
import json
import random
import csv
import logging

from transport_type import TransportType
from means_of_transport.personal_transport import PersonalTransport

NUM_MOTOR_SCOOTERS = 153  # from mobility app
MIN_LAT = 47.347671
MAX_LAT = 47.399130
MIN_LONG = 8.497557
MAX_LONG = 8.564475
SEED = 42


DATA_PATH = "../../data/mobility.csv"


def read_mobility_motor_scooters():
    type = TransportType.MOTOR_SCOOTER
    company = 'mobility'
    mobility_motor_scooters = []
    with open(DATA_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count==0:
                pass
            elif len(row) >= 2:
                # Note: in this data set first column is unusually a longitude
                long = row[0]
                lat = row[1]
                mobility_motor_scooters.append(PersonalTransport(type=type, company=company, lat=lat, long=long))
            line_count += 1

        return mobility_motor_scooters


if __name__ == "__main__":
    hack_zurich_lat = 47.390229
    hack_zurich_long = 8.514694

    flash_scooters = read_mobility_motor_scooters()
    print(flash_scooters)