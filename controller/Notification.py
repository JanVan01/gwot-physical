import paho.mqtt.publish as publish

    # Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
    # Subscrubers of the channel 'everyMeasurement' will recieve
def publishEveryMeasurement(data):
    message = str(data).encode('unicode_escape')
    publish.single("everyMeasurement", message.value, hostname="localhost")
