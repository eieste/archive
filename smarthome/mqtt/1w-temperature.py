import argparse
import json
import logging
import os
import re
import time
from datetime import datetime
from glob import glob

import paho.mqtt.client as mqtt

log = logging.getLogger(__name__)

# Folder with 1-Wire devices
w1DeviceFolder = '/sys/bus/w1/devices'


class Command:

    def __init__(self, parser=None):
        if parser is None:
            parser = argparse.ArgumentParser()
        self.parser = parser

    def add_arguments(self, parser=None):
        if parser is None:
            parser = self.parser
        parser.add_argument("--log-level", type=str, default="INFO", help="Chnage application loglevel")
        parser.add_argument("--mqtt-broker", type=str, default=os.environ.get("MQTT_BROKER"),
                            help="MQTT broker address")
        parser.add_argument("--mqtt-port", type=int, default=os.environ.get("MQTT_PORT", 1883), help="MQTT broker port")
        parser.add_argument("--mqtt-topic", type=str, default=os.environ.get("MQTT_TOPIC"), help="MQTT topic")
        parser.add_argument("-s", "--simulate", action="store_true",
                            help="it connects to mqtt and to the flower but it doesnt publish a message")
        parser.add_argument("-r", "--run", action="store_true", help="Activate application loop")
        parser.add_argument("-i", "--interval", type=int, default=os.environ.get("INTERVAL", 10),
                            help="Interval between publish")
        parser.add_argument("--scan", action="store_true", help="Scan Bluetooth devices")

    def parse(self, parser=None):
        if parser is None:
            parser = self.parser
        args = parser.parse_args()
        return args

    @staticmethod
    def find_thermometers():
        # Get all devices
        w1Devices = glob(w1DeviceFolder + '/*/')
        # Create regular expression to filter only those starting with '28', which is thermometer
        w1ThermometerCode = re.compile(r'28-\d+')
        # Initialize the array
        thermometers = []
        # Go through all devices
        for device in w1Devices:
            # Read the device code
            deviceCode = device[len(w1DeviceFolder) + 1:-1]
            # If the code matches thermometer code add it to the array
            if w1ThermometerCode.match(deviceCode):
                thermometers.append(deviceCode)
        # Return the array
        return thermometers

    @staticmethod
    def read_temp_raw(deviceCode):
        f = open(w1DeviceFolder + '/' + deviceCode + '/w1_slave', 'r')
        lines = f.readlines()
        f.close()
        return lines

    @staticmethod
    def read_temp(deviceCode):
        # Read the raw temperature data
        lines = Command.read_temp_raw(deviceCode)
        # Wait until the data is valid - end of the first line reads 'YES'
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = Command.read_temp_raw(deviceCode)
        # Read the temperature, that is on the second line
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            # Convert the temperature number to Celsius
            temp_c = float(temp_string) / 1000.0
            # Return formatted sensor data
            return deviceCode, temp_c

    def get_temperatures(self):
        temps = {}
        thermometers = Command.find_thermometers()
        # Go through all connected thermometers
        for thermometer in thermometers:
            key, value = Command.read_temp(thermometer)
            temps[key] = value
        return temps

    def on_connect(self):
        pass

    @staticmethod
    def print_temperature(temps):
        print('|________')
        print('|')
        for key, value in temps.items():
            print('| {} => {}'.format(key, value))

    def handle(self, options):

        if options.interval < 5:
            raise ValueError("--interval MUST be greate than 5")

        log.debug("Options: %s", options)

        if options.log_level:
            logging.basicConfig(level=getattr(logging, options.log_level.upper()))

        if options.run or options.simulate:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            log.info("Connect to Mqtt")
            client.connect(options.mqtt_broker, options.mqtt_port, 60)
            log.info("Initial Read")
            temps = self.get_temperatures()

            if options.simulate:
                Command.print_temperature(temps)

            if options.run:
                while True:
                    temps = self.get_temperatures()
                    for key, value in temps.items():
                        client.publish("{topic}/{key}".format(topic=options.mqtt_topic, key=key), json.dumps({
                            "celsis": value,
                            "fahrenheit": (value * 9 / 5) + 32,
                            "timestamp": datetime.now().isoformat()}
                        ))

                    time.sleep(options.interval)

            client.loop_forever()


if __name__ == "__main__":
    cmd = Command()
    cmd.add_arguments()
    options = cmd.parse()
    cmd.handle(options)
