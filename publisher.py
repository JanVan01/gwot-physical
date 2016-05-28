import paho.mqtt.publish as publish
import json
from datetime import datetime
from database.database import Database
from flask import Flask, Response, request

################################################
# Duplicated: Has to be solved
################################################
def get_filter():


    args = {
        'outliers': None,
        'start': None,
        'end': None,
        'location': None,
        'coordinates': None
    }



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

##################################################################################################



db = Database()

data = db.get_last_measurement(get_filter())
publish("everyMinute", data, hostname="localhost")


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
