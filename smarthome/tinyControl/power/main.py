from power.power_monitor import PowerMonitor
import logging


log = logging.getLogger("PowerModule")


def start():
    log.info("Start Broadlink Powermonitor")
    power_monitor = PowerMonitor(name="Broadlink-Monitor")
    power_monitor.start()


if __name__ == "__main__":
    start()