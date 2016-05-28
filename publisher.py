import paho.mqtt.publish as publish
from database.database import Database

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


db = Database()

data = db.get_last_measurement(get_filter())
message = str(data).encode('string_escape')

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
