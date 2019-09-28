import os

from flask import Flask, request, jsonify

from means_of_transport.functions import get_filtered_personal_transport_output_list
from directions import get_routes_for_transport_types

# Initialize Flask app
app = Flask(__name__)

DEFAULT_RADIUS_KM = 2.0


@app.route('/neighbourhood')
def neighbourhood():
    start_long = request.args.get('start_long', type=float)
    start_lat = request.args.get('start_lat', type=float)
    radius = request.args.get('radius', type=float, default=DEFAULT_RADIUS_KM)
    personal_transport_output_list = get_filtered_personal_transport_output_list(
        user_lat=start_lat,
        user_long=start_long,
        radius=radius
    )
    return jsonify(results=personal_transport_output_list)


@app.route('/directions')
def directions():
    start_long = request.args.get('start_long', type=float)
    start_lat = request.args.get('start_lat', type=float)
    end_long = request.args.get('end_long', type=float)
    end_lat = request.args.get('end_lat', type=float)
    routes = get_routes_for_transport_types(start_lat, start_long, end_lat, end_long)
    return jsonify(results=routes)


@app.route('/')
def hello_world():
    return "Hello World!"


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
