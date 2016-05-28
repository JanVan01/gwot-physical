import paho.mqtt.publish as publish
import json
from datetime import datetime
from flask import Flask, Response, request
from database.database import Database
from sensor.sensor import Sensor



app = Flask(__name__)
sensor = Sensor()
db = Database()

data = db.get_last_measurement(server.get_filter())
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
