from means_of_transport.transport_type_mapping import TRANSPORT_TYPE_TO_OUTPUT_TYPE


class PersonalTransport(object):
    def __init__(self, type, company, lat, long):
        self.type = type
        self.company = company
        self.lat = lat
        self.long = long

    def get_output_dict(self):
        output_dict = {
            'type': TRANSPORT_TYPE_TO_OUTPUT_TYPE[self.type],
            'company': self.company,
            'lat': self.lat,
            'long': self.long
        }
        return output_dict

    def to_str(self):
        return f"type={TRANSPORT_TYPE_TO_OUTPUT_TYPE[self.type]}|company={self.company}|lat={self.lat}|long={self.long}"

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()
