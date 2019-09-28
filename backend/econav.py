import os

from flask import Flask
import enum

# Initialize Flask app
app = Flask(__name__)


class TransportType(enum.Enum):
    E_BIKE = 0,
    E_CAR = 1,
    E_SCOOTER = 2,
    BIKE = 3,
    WALK = 4


@app.route('/')
def hello_world():
    return "Hello World!"


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
