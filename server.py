import json
from datetime import datetime
from flask import Flask, Response, request
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
    data = db.get_last_measurement(get_filter())
    return send_json(data)

@app.route('/api/data/list')
def data_list():
    data = db.get_measurement_list(get_filter())
    return send_json(data)

@app.route('/api/data/min')
def data_min():
    data = db.get_min_measuremen(get_filter())
    return send_json(data)

@app.route('/api/data/max')
def data_max():
    data = db.get_max_measurement(get_filter())
    return send_json(data)

@app.route('/api/location/list')
def location_list():
    data = db.get_location_list()
    return send_json(data)

def get_filter():
    # ToDo: Add proper variable checks / sanitation
    outliers = request.args.get('outliers')
    start = request.args.get('start')
    end = request.args.get('end')
    location = request.args.get('location')
    coordinates = request.args.get('coordinates')
    
    args = {
        'outliers': None,
        'start': None,
        'end': None,
        'location': None,
        'coordinates': None
    }

    if outliers != None and len(outliers) > 0 and (outliers == 0 or outliers == 1):
        args['outliers'] = outliers
    
    # ToDo
    if start != None and len(start) > 0:
        args['start'] = start

    # ToDo
    if end != None and len(end) > 0:
        args['end'] = end

    if location != None and location > 0:
        args['location'] = location

    # ToDo
    if coordinates != None and len(coordinates) > 0:
        args['coordinates'] = coordinates
        
    return args
        

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
