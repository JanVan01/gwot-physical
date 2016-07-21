from utils.utils import SettingManager # Inport SettingManager for HTML output
from sensors.base import BaseSensor, SensorMeasurement # Include BaseSensor and SensorMeasurement classes
import os # Import os module for getting the load average

# We call our class LoadAverageSensor and derive it from BaseSensor
class LoadAverageSensor(BaseSensor):

	 # Returns a name of the used sensor as string
	def get_type(self):
		return "LoadAvg"
	
	# Returns the unit of the values measured
	def get_unit(self):
		# Actually the load average has no real unit, therefore we leave it empty.
		return ""
	
	# Here the measurement is taking place.
	# It returns a SensorMeasurement object containing the measured value and a quality between 0.0 (worst) and 1.0 (best).
	# The quality should express the accuracy of the value.
	def get_measurement(self):
		# Returns a list of three values stating the load average in the last one, five and fifteen minutes. 
		load_values = os.getloadavg()
		# Get the setting to know which interval to measure
		length = self.get_setting('avg_length')
		# The quality is always stated as best (1.0) as they are always exact
		return SensorMeasurement(load_values[int(length)], 1.0)

	# Returns a boolean stating true in case a measurement should be taken, false if not
	def is_due(self, minutes, interval):
		length = self.get_setting('avg_length')
		# Suit the interval to the kind of load average we are measuring
		if length == "0":
			interval = 1
		elif length == "1":
			interval = 5
		elif length == "2":
			interval = 15
		return super().is_due(minutes, interval)

	# Returns all setting identifiers that are supported.
	def get_setting_keys(self):
		return ["avg_length"]
	
	# Returns the title for the UI for the specified setting identifier
	def get_setting_name(self, key):
		# For the setting identifier 'avg_length' return the title
		if key == 'avg_length':
			return "Load average time frame"
		else:
			return None
	
	# Input validation of the value for the user specified data
	def validate_setting(self, key, value):
		# Check for the setting identifier 'avg_length' whether the value is one of 0, 1 or 2
		if key == 'avg_length' and (value == "0" or value == "1" or value == "2"):
			return True
		else:
			return False
	
	# Returns the HTML component where the user can input his data
	def get_setting_html(self, key, value = None):
		# Specify the values for a select element as touples in a list.
		# The first element is the internal value you can use in your code, the second element is the visible title for the option.
		values = [["0", "1 min average"], ["1", "5 min average"], ["2", "15 min average"]]
		return SettingManager().get_select_field(key, values, value)

	# Returns the number of decimals that are relevant for low precision use, e.g. trend calculation.
	def low_precision(self):
		return 1