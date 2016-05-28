import paho.mqtt.publish as publish
import json
from datetime import datetime
from database.database import Database
from flask import Flask, Response, request


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



db = Database()

data = db.get_last_measurement(get_filter())
publish.single("everyMinute", "send_json(data)", hostname="localhost")


# publish.single("everyMeasurement","everyMeasurementMessage", hostname="localhost")
#
# publish.single("every5Minutes","every5MinutesMessage", hostname="localhost")
#
# publish.single("every10Minutes","every10MinutesMessage", hostname="localhost")
#
# publish.single("every15Minutes","every15MinutesMessage", hostname="localhost")
#
# publish.single("every30Minutes","every30MinutesMessage", hostname="localhost")
#
# publish.single("every45Minutes","every45MinutesMessage", hostname="localhost")
#
# publish.single("daylyReport","daylyReport", hostname="localhost")
