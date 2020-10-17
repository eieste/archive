import paho.mqtt.client as mqttlib
from utils.conf import settings
import logging
from plugin.colorset import Colorset


log = logging.getLogger("mqttclient")

plugin_list = [
    Colorset()
]

class Mqtt(mqttlib.Client):

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, *args, **kwargs):
        for plugin in plugin_list:
            self.subscribe(plugin.topic)

    def on_message(self, m, userdata, msg): # *args, **kwargs):
        for plugin in plugin_list:
            print(msg.topic)
            print(plugin.topic)
            if msg.topic == plugin.topic:
                plugin.on_message(msg.topic, msg.payload)
