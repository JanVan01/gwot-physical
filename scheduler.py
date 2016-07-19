#!/usr/bin/python3

# Sensor trigger executed by cron job

import sys
assert sys.version_info >= (3,0)
from utils.utils import OS
from models.sensors import Sensors
from views.json import JSON
from utils.utils import ThreadObserver

if __name__ == '__main__':
	OS().cwd(__file__)

	# Trigger sensors and save all sensor readings
	sensors = Sensors()
	data = sensors.trigger_pending()
	# Send json to cmd line for debugging
	json = JSON()
	print(json.build(data))

	ThreadObserver.Instance().wait()
