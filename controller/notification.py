import paho.mqtt.publish as publish # needed to push messages to subscribers
#import json # needed to construct the output and return a json

    # Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
    # Subscrubers of the channel 'everyMeasurement' will recieve

# Todo: Consturct response with loop over list
def publishMeasurement(data):
    publishEveryMeasurement(data)
    publishByThreshold(data)

def publishEveryMeasurement(data):
    # data = []
    # for i in range(len(data)):
    #     sensor_data = {} # new object to be passed to data
    #     data[i].

    message = str(data).encode('unicode_escape')
    publish.single("everyMeasurement", message, hostname="localhost")

def publishByThreshold(data):
    if data[0].value > 200:
        message = str(data[0].value).encode('unicode_escape')
        publish.single("publishByThreshold", message, hostname="localhost")
