import socket
import threading
import time
import json
import logging
from control.control_parameters import ControlParameters
from settings import conf
import re


import requests


log = logging.getLogger("ControlMgr")

KV_REG = re.compile(r'((?:\\.|[^=,]+)*)=(\"(?:\\.|[^\"\\]+)*\"|(?:\\.|[^,\"\\]+)*)')


class ControlManager(threading.Thread):

    def test_api_ip(self):

        if not ControlParameters.API_IP:
            log.debug("Parameter API_IP is empty")
            return False
        try:
            requests.get("http://"+ControlParameters.API_IP+""+conf.FLAT_API_PORT+"/ht/")
        except Exception as e:
            log.warning("Cant reach API IP healthcheck")
            log.error(e)
            return False
        return True

    @classmethod
    def broadcast(self, key, value):
        data = "{}=\"{}\"".format(key, value)

        ControlParameters._socket.sendto(data.encode("UTF-8"), ("255.255.255.255", conf.CONTROL_MGR_PORT))

    def run(self):

        while True:

            if not self.test_api_ip():
                log.info("Request missing parameter API_IP")
                ControlManager.broadcast("MISSING", "API_IP")

            time.sleep(5)

