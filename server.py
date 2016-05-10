import json
from datetime import datetime
from flask import Flask, Response
from database.database import Database
from sensor.sensor import Sensor


app = Flask(__name__)
sensor = Sensor()
db = Database()


@app.route('/api/data/trigger')
def data_trigger():
    location = 1 # ToDO: to be set properly
    value = sensor.trigger_reading()
    data = db.save_measurement(value, location)
    return send_json(data)

@app.route('/api/data/last')
def data_last():
    data = db.get_last_measurement()
    return send_json(data)

@app.route('/api/data/list')
def data_list():
    data = db.get_measurement_list()
    return send_json(data)

@app.route('/api/data/min')
def data_min():
    data = db.get_min_measuremen()
    return send_json(data)

@app.route('/api/data/max')
def data_max():
    data = db.get_max_measurement()
    return send_json(data)


def send_json(data):
    body = json.dumps(data, default=json_serial)
    resp = Response(body, status=200, mimetype='application/json')
    return resp;

# JSON serializer for objects not serializable by default json code
def json_serial(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
