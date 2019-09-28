import os
import json
import enum

from flask import Flask, request, jsonify

from backend.means_of_transport.functions import get_personal_transport_output_list

# Initialize Flask app
app = Flask(__name__)


class TransportType(enum.Enum):
    E_BIKE = 0,
    E_CAR = 1,
    E_SCOOTER = 2,
    BIKE = 3,
    WALK = 4


@app.route('/neighbourhood')
def neighbourhood():
    start_long = request.args.get('start_long', type=float)
    start_lat = request.args.get('start_lat', type=float)
    personal_transport_output_list = get_personal_transport_output_list(start_long, start_lat)
    return jsonify(results=personal_transport_output_list)


@app.route('/')
def hello_world():
    return "Hello World!"


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
