import paho.mqtt.client as mqtt
from utils.conf import settings
import logging

log = logging.getLogger("mqttclient")


class Mqtt:

    def connect(self):
        self._client = mqtt.Client()
        self._client.on_connect = Mqtt.on_connect
        self._client.on_message = Mqtt.on_message
        self._client.connect(settings.MQTT_HOST, 1883, 60)
        self._client.loop_forever()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        log.info("Connected with result code "+str(rc))

        client.subscribe("{}/{}".format(settings.MQTT_TOPIC, "led/color"))

    def on_message(self, userdata, msg):
        print(userdata)
        print(msg)
        # print(msg.topic+" "+str(msg.payload))
