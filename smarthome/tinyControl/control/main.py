from control.control_server import ControlServer
from control.control_manager import ControlManager
from control.control_parameters import ControlParameters
from settings import conf
import socket


def start():

    ControlParameters._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ControlParameters._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    config_receive = ControlServer()
    config_receive.start()

    config_check = ControlManager()
    config_check.start()
