# from broadlink import sp2
#
# dev = sp2( ("192.168.69.42", 80), "34:EA:34:E4:0B:34", 38010)
#
# print(dev.auth())
# print(dev.get_energy())
# print(dev.check_power())
# dev.set_power(False)

from controller import *

device = find_device("apu-board", DEVICE_LIST)
remote_command(device)