import paho.mqtt.client as mqtt
from models.config import ConfigManager
from utils.utils import Singleton

@Singleton
class DangerListener(object):

    def __init__(self):
        self.state = 'ok'
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect('localhost')
        self.client.loop_start()

    def reset_connection(self, url):
        self.client.disconnect()
        self.client.connect(url)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("test")

    def on_message(self, client, userdata, msg):
        if str(msg.payload) == 'ok':
            self.state = 'ok'
        elif str(msg.payload) == 'danger':
            self.state = 'danger'
