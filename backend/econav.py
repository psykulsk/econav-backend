import os
import json
import enum

from flask import Flask, request, jsonify

from means_of_transport.functions import get_personal_transport_output_list

# Initialize Flask app
app = Flask(__name__)


@app.route('/neighbourhood')
def neighbourhood():
    start_long = request.args.get('start_long', type=float)
    start_lat = request.args.get('start_lat', type=float)
    personal_transport_output_list = get_personal_transport_output_list(
        user_lat=start_lat,
        user_long=start_long
    )
    return jsonify(results=personal_transport_output_list)


@app.route('/directions')
def directions():
    start_long = request.args.get('start_long', type=float)
    start_lat = request.args.get('start_lat', type=float)
    end_long = request.args.get('end_long', type=float)
    end_lat = request.args.get('end_lat', type=float)

    return jsonify(results=[])


@app.route('/')
def hello_world():
    return "Hello World!"


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
