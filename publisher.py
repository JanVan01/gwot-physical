import sys
assert sys.version_info >= (3,0)

import paho.mqtt.publish as publish
#from models.database import Database # intentionally?

from models.config import Database
from models.measurements import Measurements

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

##################################################################################################

db = Database().connect()
measurements = Measurements(db)
data = measurements.get_last(get_filter()) # ToDo: Convert data to JSON?
message = str(data).encode('unicode_escape')


###################################################################################################
# Channels related to Time
####################################################################################################
publish.single("everyMinute", message, hostname="localhost")

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
#####################################################################################################
#####################################################################################################
# Channels related to events
#####################################################################################################
# publish.single("IncreaseBy>=0.1mFromMean","IncreaseBy>=0.1mFromMean", hostname="localhost")
#
# publish.single("IncreaseBy>=0.25mFromMean","IncreaseBy>=0.25mFromMean", hostname="localhost")
####################################################################################################
#####################################################################################################
# Channels related to increasing events and time
#####################################################################################################
# publish.single("IncreaseBy>=0.1mIn1Minute","IncreaseBy>=0.1mIn1Minute", hostname="localhost") # It can be fast: https://www.youtube.com/watch?v=dfRfE8iJPRo
#
# publish.single("IncreaseBy>=0.1mIn5Minute","IncreaseBy>=0.1mIn5Minute", hostname="localhost")
#
# publish.single("IncreaseBy>=0.1mIn10Minute","IncreaseBy>=0.1mIn10Minute", hostname="localhost")
#
# publish.single("IncreaseBy>=0.1mIn15Minute","IncreaseBy>=0.1mIn15Minute", hostname="localhost")
#
# publish.single("IncreaseBy>=0.1mIn20Minute","IncreaseBy>=0.1mIn20Minute", hostname="localhost")
#
# publish.single("IncreaseBy>=0.1mIn30Minute","IncreaseBy>=0.1mIn30Minute", hostname="localhost")
#####################################################################################################
#####################################################################################################
# Channels related to decreasing events
#####################################################################################################
# publish.single("DecreaseBy>=0.25m","DecreaseBy>=0.25m", hostname="localhost")
#
# publish.single("DecreaseBy>=0.5m","DecreaseBy>=0.5m", hostname="localhost")
####################################################################################################
#####################################################################################################
# Channels related to events and time
#####################################################################################################
# publish.single("DecreaseBy>=0.1mIn1Minute","DecreaseBy>=0.1mIn1Minute", hostname="localhost")
#
# publish.single("DecreaseBy>=0.1mIn5Minute","DecreaseBy>=0.1mIn5Minute", hostname="localhost")
#
# publish.single("DecreaseBy>=0.1mIn10Minute","DecreaseBy>=0.1mIn10Minute", hostname="localhost")

# publish.single("DecreaseBy>=0.1mIn15Minute","DecreaseBy>=0.1mIn15Minute", hostname="localhost")
#
# publish.single("DecreaseBy>=0.1mIn20Minute","DecreaseBy>=0.1mIn20Minute", hostname="localhost")
#
# publish.single("DecreaseBy>=0.1mIn30Minute","DecreaseBy>=0.1mIn30Minute", hostname="localhost")
####################################################################################################
