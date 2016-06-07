#!/usr/bin/python3

# Sensor trigger executed by cron job

import sys
assert sys.version_info >= (3,0)

from models.config import Database
from models.sensors import Sensors
from views.json import JSON

if __name__ == '__main__':
	# Connect to database; trigger and save all sensor readings
	db = Database().connect()
	sensors = Sensors(db)
	data = sensors.trigger_all()
	# Send json to cmd line for debugging
	json = JSON()
	print(json.build(data))