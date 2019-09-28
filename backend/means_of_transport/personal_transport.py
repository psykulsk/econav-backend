import json


class PersonalTransport(object):
    def __init__(self, type, company, long, lat):
        self.type = type
        self.company = company
        self.long = long
        self.lat = lat

    def get_json(self):
        output_dict = {
            'type': self.type,
            'company': self.company,
            'long': self.long,
            'lat': self.lat
        }
        return json.dumps(output_dict)
