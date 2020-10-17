import RPi.GPIO as GPIO
import time
import requests
import json
from thread import start_new_thread
import time
import pigpio
from datetime import datetime, timedelta
from collections import namedtuple
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Color:

    def __init__(self, r, g, b):
        self.R = float(r)
        self.G = float(g)
        self.B = float(b)

class RuntimeData:
    SUNSET = -1 #Sonnenuntergang
    SUNRISE = -1 #Sonnenaufgang
    LED_STATE = False
    LAST_MOVEMENT = -1


# Configuration

ANIMATION_STEPS = 50    # Count of steps
ANIMATION_TIME = 0.2    # Time between animation steps
SENSOR_PIN = 18         # PIN of movement Sensor
LNG = 13.404954         # Geo Position
LAT = 52.520008

ONTIME = {"minutes": 1}         # Duration, how long the light is on
pin_setup = {"r": 22, "g":24, "b":17}    # PINS of LED Stripes

MAX_COLOR = Color(20, 0, 0)           # Color to be reached after release

## Configuration END

RUNTIME = RuntimeData()

PIN = namedtuple("PINS", pin_setup.keys())(*pin_setup.values())

pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def event_callback(channel):
    logger.info("Movement Detected")

    RUNTIME.LAST_MOVEMENT = datetime.now()

    if not RUNTIME.LED_STATE:
        if datetime.now() > RUNTIME.SUNSET or datetime.now() < RUNTIME.SUNRISE:
            logger.info("Night Detected")
            logger.info("Start Light Circle")
            start_new_thread(light, (RUNTIME,))
        else:
            logger.info("Currently is Day")

def color(r, g, b):
    pi.set_PWM_dutycycle(PIN.r, r)
    pi.set_PWM_dutycycle(PIN.g, g)
    pi.set_PWM_dutycycle(PIN.b, b)

def light(runtime):
    runtime.LED_STATE = True
    stepsize = Color(MAX_COLOR.R/ANIMATION_STEPS, MAX_COLOR.G/ANIMATION_STEPS, MAX_COLOR.B/ANIMATION_STEPS)
    current = Color(0, 0, 0)

    logger.info("Glow UP")

    for i in range(1, ANIMATION_STEPS):
        color(current.R, current.G, current.B)
        current.R = current.R+stepsize.R
        current.G = current.G+stepsize.G
        current.B = current.B+stepsize.B
        fix(current)
        color(current.R, current.G, current.B)
        time.sleep(ANIMATION_TIME)

    runtime.LAST_MOVEMENT = datetime.now()
    start_light_hold = runtime.LAST_MOVEMENT

    logger.info("Hold light for {}".format(ONTIME))
    while datetime.now()-timedelta(**ONTIME) < runtime.LAST_MOVEMENT:
        countdown = runtime.LAST_MOVEMENT-(datetime.now()-timedelta(**ONTIME))

        if start_light_hold < runtime.LAST_MOVEMENT:
            logger.info("Keep the light on for more {}".format(countdown))
            start_light_hold = runtime.LAST_MOVEMENT
        else:
            logger.info("Light is on for {} ".format(countdown))

        time.sleep(5)


    for i in range(0, ANIMATION_STEPS):
        color(current.R, current.G, current.B)
        current.R = current.R-stepsize.R
        current.G = current.G-stepsize.G
        current.B = current.B-stepsize.B

        fix(current)

        color(current.R, current.G, current.B)
        time.sleep(ANIMATION_TIME)
    runtime.LED_STATE = False

def fix(obj):
    if obj.R < 0:
        obj.R = 0
    if obj.G < 0:
        obj.G = 0
    if obj.B < 0:
        obj.B = 0

    if obj.R > 255:
        obj.R = 255
    if obj.G > 255:
        obj.G = 255
    if obj.B > 255:
        obj.B = 255

def sunrise_sunset_update(runtime):
    API_URL = "https://api.sunrise-sunset.org/json?lat={}&lng={}&date=today".format(LAT, LNG)
    while True:
        response = requests.get(API_URL)
        data = json.loads(response.text)
        now = datetime.now()

        runtime.SUNRISE = datetime.strptime("{}-{}-{} {}".format(now.year, now.month, now.day, data["results"]["sunrise"]), "%Y-%m-%d %I:%M:%S %p")
        runtime.SUNSET = datetime.strptime("{}-{}-{} {}".format(now.year, now.month, now.day, data["results"]["sunset"]), "%Y-%m-%d %I:%M:%S %p")
        logger.info("SunSET and SunRise Updated")
        time.sleep(60*60*12)


if __name__ == '__main__':
    try:
        start_new_thread(sunrise_sunset_update, (RUNTIME,))
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=event_callback)
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print
        "Beende..."

    GPIO.cleanup()

