from collections import namedtuple
from broadlink import sp2
import paramiko
import os
import socket
import time
import logging

log = logging.getLogger("controller")

log.setLevel(logging.DEBUG)


Device = namedtuple("Device", ("name", "ip", "mac", "depends", "username", "cmd_poweroff", "apu_iface"))

DeviceList = namedtuple("DeviceList", ("apu", "usg", "workstation", "storageone", "storagetwo", "ap"))

DEVICE_LIST = DeviceList(
    Device("DEIVCE NAME", "IPADDRESS", "MACADDRESS", (), "USERNAME", "COMMAND", ""),
)

PowerSocket = namedtuple("PowerSocket", ("name", "ip", "mac", "editable"))

SOCKET_LIST = [
    PowerSocket("DEVICENAME", "IPADDRESS", "MACADDRESS", False )
]


def socket_set_state(socket_list, new_state):
    for socket in socket_list:
        if socket.editable:
            device = sp2( (socket.ip, 80), socket.mac, devtype=38010)
            device.auth()
            device.set_power(new_state)

def socket_get_state(socket_list):
    result = {}
    for socket in socket_list:
        if socket.editable:
            device = sp2( (socket.ip, 80), socket.mac, devtype=38010)
            device.auth()
            result[socket.name] = device.check_power()
    return result

def socket_get_energy(socket_list):
    result = {}
    for socket in socket_list:
        device = sp2( (socket.ip, 80), socket.mac, devtype=38010)
        device.auth()
        result[socket.name] = device.get_energy()
    return result

def find_sockets_by_names(names):
    res = []
    for sock in SOCKET_LIST:
        if sock.name.lower() in [ n.lower() for n in names ]:
            res.append(sock)
    return res


def find_device(name):

    for device in DEVICE_LIST:

        if device.name == name:
            return device
    if hasattr(DEVICE_LIST, name):
        return getattr(DEVICE_LIST, name)



def remote_command(device, command):
    client = paramiko.SSHClient()
    k = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(device.ip, username=device.username, pkey=k)
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read())
    print(stderr.read())
    client.close()

    return (
        stdout.read().decode(),
        stderr.read().decode(),
    )

def remote_wol(device):
    print(f"etherwake -i {device.apu_iface} {device.mac}")
    return remote_command(find_device("apu-board"), f"etherwake -i {device.apu_iface} {device.mac}")


def poweroff(device):
    return remote_command(device, device.cmd_poweroff)


def is_open(ip, port, timeout=121):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(timeout)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False
