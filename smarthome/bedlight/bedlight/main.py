from core.mqtt import Mqtt
from utils.conf import settings

mqtt = Mqtt()
mqtt.connect(settings.MQTT_HOST, 1883, 60)
mqtt.loop_forever()
