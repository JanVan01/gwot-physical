# Sensor trigger executed by cron job

import sys
assert sys.version_info >= (3,0)

from models.sensor import Sensor
from models.database import Database

sensor = Sensor()
db = Database()

location = 1 # ToDo add current location from config
value = sensor.trigger_reading()
db.save_measurement(value, location)