import json


class PersonalTransport(object):
    def __init__(self, type, company, long, lat):
        self.type = type
        self.company = company
        self.long = long
        self.lat = lat

    def get_output_dict(self):
        output_dict = {
            'type': self.type,
            'company': self.company,
            'long': self.long,
            'lat': self.lat
        }
        return output_dict
