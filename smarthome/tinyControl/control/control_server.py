import socket
import threading
import time
import json
import logging
from settings import conf
import re
from control.control_parameters import ControlParameters

log = logging.getLogger("ControlSrv")

KV_REG = re.compile(r'((?:\\.|[^=,]+)*)=(\"(?:\\.|[^\"\\]+)*\"|(?:\\.|[^,\"\\]+)*)')


class ControlServer(threading.Thread):

    def run(self):
        ControlParameters._socket.bind(("", conf.CONTROL_MGR_PORT))
        log.info("Start recv loop")
        while True:
            content = ControlParameters._socket.recvfrom(1024)
            self.parse(*content)

    def parse(self, content, addr):

        data = content.decode("UTF-8")
        data = data.strip()

        result = KV_REG.search(data)
        key = result.group(1).strip().lower()
        value = result.group(2).strip().strip('"').strip()

        if key == "api_ip":
            log.debug("Set Parameter api_ip")
            ControlParameters.API_IP = value