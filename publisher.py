import paho.mqtt.publish as publish
#publish.single("paho/test/single", "boo", hostname="test.mosquitto.org")
publish.single("everyMeasurement","everyMeasurementMessage", hostname="localhost")

publish.single("every5Minutes","every5MinutesMessage", hostname="localhost")

publish.single("every10Minutes","every10MinutesMessage", hostname="localhost")

publish.single("every15Minutes","every15MinutesMessage", hostname="localhost")

publish.single("every30Minutes","every30MinutesMessage", hostname="localhost")

publish.single("every45Minutes","every45MinutesMessage", hostname="localhost")

publish.single("daylyReport","daylyReport", hostname="localhost")

publish.single("daylyReport","daylyReport", hostname="localhost")
