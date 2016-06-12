from controller.base import BaseController
import paho.mqtt.publish as publish

class Notification(BaseController):

    # Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
    # Subscrubers of the channel 'everyMeasurement' will recieve the data.
    def publishEveryMeasurement(self, data){
        message = str(data).encode('unicode_escape')
        publish.single("everyMeasurement", message, hostname="localhost")
    }
