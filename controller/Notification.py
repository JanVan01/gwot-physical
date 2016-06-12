import paho.mqtt.publish as publish

    # Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
    # Subscrubers of the channel 'everyMeasurement' will recieve

def publish Measurement(data):
    publishEveryMeasurement(data)
    publishByThreshold(data)

def publishEveryMeasurement(data):
    message = str(data[0].value).encode('unicode_escape')
    publish.single("everyMeasurement", message, hostname="localhost")

def publishByThreshold((data):
    if(data[0].value > 200)
        message = str(data[0].value).encode('unicode_escape')
        publish.single("publishByThreshold", message, hostname="localhost")
