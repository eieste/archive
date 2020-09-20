#!/usr/bin/python

import random
import socket
import binascii
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class sp2:

    def __init__(self, host, mac, devtype, timeout=10):
        self.host = host
        self.mac = sp2.convert_mac_address(mac)
        self.timeout = timeout
        self.devtype = devtype
        self.count = random.randrange(0xffff)
        self.iv = bytearray(
            [0x56, 0x2e, 0x17, 0x99, 0x6d, 0x09, 0x3d, 0x28, 0xdd, 0xb3, 0xba, 0x69, 0x5a, 0x2e, 0x6f, 0x58])
        self.id = bytearray([0, 0, 0, 0])
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.cs.bind(("", 1234))
        self.type = "SP2"
        self.aes = None
        key = bytearray(
            [0x09, 0x76, 0x28, 0x34, 0x3f, 0xe9, 0x9e, 0x23, 0x76, 0x5c, 0x15, 0x13, 0xac, 0xcf, 0x8b, 0x02])
        self.update_aes(key)

    @staticmethod
    def convert_mac_address(address):
        digit_list = address.split(":")
        digit_list.reverse()
        hex_str = "".join(digit_list)
        return binascii.unhexlify(hex_str)


    def update_aes(self, key):
        self.aes = Cipher(algorithms.AES(key), modes.CBC(self.iv),
                          backend=default_backend())

    def encrypt(self, payload):
        encryptor = self.aes.encryptor()
        return encryptor.update(payload) + encryptor.finalize()

    def decrypt(self, payload):
        decryptor = self.aes.decryptor()
        return decryptor.update(payload) + decryptor.finalize()

    def auth(self):
        payload = bytearray(0x50)
        payload[0x04] = 0x31
        payload[0x05] = 0x31
        payload[0x06] = 0x31
        payload[0x07] = 0x31
        payload[0x08] = 0x31
        payload[0x09] = 0x31
        payload[0x0a] = 0x31
        payload[0x0b] = 0x31
        payload[0x0c] = 0x31
        payload[0x0d] = 0x31
        payload[0x0e] = 0x31
        payload[0x0f] = 0x31
        payload[0x10] = 0x31
        payload[0x11] = 0x31
        payload[0x12] = 0x31
        payload[0x1e] = 0x01
        payload[0x2d] = 0x01
        payload[0x30] = ord('T')
        payload[0x31] = ord('e')
        payload[0x32] = ord('s')
        payload[0x33] = ord('t')
        payload[0x34] = ord(' ')
        payload[0x35] = ord(' ')
        payload[0x36] = ord('1')

        response = self.send_packet(0x65, payload)
        payload = self.decrypt(response[0x38:])

        if not payload:
            return False

        key = payload[0x04:0x14]
        if len(key) % 16 != 0:
            return False

        self.id = payload[0x00:0x04]
        self.update_aes(key)
        return True

    def send_packet(self, command, payload):
        self.count = (self.count + 1) & 0xffff
        packet = bytearray(0x38)
        packet[0x00] = 0x5a
        packet[0x01] = 0xa5
        packet[0x02] = 0xaa
        packet[0x03] = 0x55
        packet[0x04] = 0x5a
        packet[0x05] = 0xa5
        packet[0x06] = 0xaa
        packet[0x07] = 0x55
        packet[0x24] = self.devtype & 0xff
        packet[0x25] = self.devtype >> 8
        packet[0x26] = command
        packet[0x28] = self.count & 0xff
        packet[0x29] = self.count >> 8
        packet[0x2a] = self.mac[0]
        packet[0x2b] = self.mac[1]
        packet[0x2c] = self.mac[2]
        packet[0x2d] = self.mac[3]
        packet[0x2e] = self.mac[4]
        packet[0x2f] = self.mac[5]
        packet[0x30] = self.id[0]
        packet[0x31] = self.id[1]
        packet[0x32] = self.id[2]
        packet[0x33] = self.id[3]

        # pad the payload for AES encryption
        if payload:
            numpad = (len(payload) // 16 + 1) * 16

            filllength = numpad-len(payload)
            payload = payload+b"\x00"*filllength

        checksum = 0xbeaf
        for i in range(len(payload)):
            checksum += payload[i]
            checksum = checksum & 0xffff

        payload = self.encrypt(payload)

        packet[0x34] = checksum & 0xff
        packet[0x35] = checksum >> 8

        for i in range(len(payload)):
            packet.append(payload[i])

        checksum = 0xbeaf
        for i in range(len(packet)):
            checksum += packet[i]
            checksum = checksum & 0xffff
        packet[0x20] = checksum & 0xff
        packet[0x21] = checksum >> 8

        start_time = time.time()
        while True:
            try:
                self.cs.sendto(packet, self.host)
                self.cs.settimeout(1)
                response = self.cs.recvfrom(2048)
                break
            except Exception as e:
                if (time.time() - start_time) > self.timeout:
                    raise e
        return bytearray(response[0])

    def set_power(self, state):
        """Sets the power state of the smart plug."""
        packet = bytearray(16)
        packet[0] = 2
        packet[4] = 1 if state else 0
        self.send_packet(0x6a, packet)

    def check_power(self):
        """Returns the power state of the smart plug."""
        packet = bytearray(16)
        packet[0] = 1
        response = self.send_packet(0x6a, packet)
        err = response[0x22] | (response[0x23] << 8)
        if err != 0:
            print("P")
            print(err)
            return None
        payload = self.decrypt(bytes(response[0x38:]))
        if isinstance(payload[0x4], int):
            return bool(payload[0x4] == 1 or payload[0x4] == 3 or payload[0x4] == 0xFD)
        return bool(ord(payload[0x4]) == 1 or ord(payload[0x4]) == 3 or ord(payload[0x4]) == 0xFD)

    def get_energy(self):
        packet = bytearray([8, 0, 254, 1, 5, 1, 0, 0, 0, 45])
        response = self.send_packet(0x6a, packet)
        err = response[0x22] | (response[0x23] << 8)
        if err != 0:
            print("E")
            print(err)
            return None
        payload = self.decrypt(bytes(response[0x38:]))
        if isinstance(payload[0x7], int):
            energy = int(hex(payload[0x07] * 256 + payload[0x06])[2:]) + int(hex(payload[0x05])[2:]) / 100.0
        else:
            energy = int(hex(ord(payload[0x07]) * 256 + ord(payload[0x06]))[2:]) + int(
                hex(ord(payload[0x05]))[2:]) / 100.0
        return energy
