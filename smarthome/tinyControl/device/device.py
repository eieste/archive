import enum
from collections import namedtuple


class DeviceType:

    def __init__(self, name, display_name):
        self._display_name = display_name
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

class DeviceAttribute:

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @staticmethod
    def generate_deviceattribute_list(attribute_dict):
        res = []
        for key, value in attribute_dict.items():
            res.append(DeviceAttribute(key, value))
        return res


class DeviceModule(enum.IntEnum):
    SP3 = 1
    SSHDevice = 2

    @staticmethod
    def resolve_modules(module_names):
        mod = []
        for name in module_names:
            if name.lower() == "sp3":
                mod.append(DeviceModule.SP3)
            if name.lower() == "ssh-device":
                mod.append(DeviceModule.SSHDevice)
        return mod


DataPoint = namedtuple("DataPoint", ("value", "datetime"))


class Device:

    DEVICE_LIST = []

    def __init__(self, id, description, device_type_dict, module_names, attribute_dict):
        self._id = id
        self._description = description
        self._device_type = DeviceType(**device_type_dict)
        self._modules = DeviceModule.resolve_modules(module_names)
        self._attributes = DeviceAttribute.generate_deviceattribute_list(attribute_dict)

    def get_attribute(self, key, flat=False):

        for attr in self._attributes:
            if attr.key.lower() == key.lower():
                if flat:
                    return attr.value
                return attr

    @staticmethod
    def find_by_module(module):
        res = []
        for device in Device.DEVICE_LIST:
            if module in device._modules:
                res.append(device)
        return res

    @staticmethod
    def get_device_by_id(id):
        for device in Device.DEVICE_LIST:
            if device._id == id:
                return device

    @staticmethod
    def update_or_create(id, description, device_type_dict, module_names, attribute_dict):

        device = Device.get_device_by_id(id)
        if device is None:
            device = Device(id, description, device_type_dict, module_names, attribute_dict)
            Device.DEVICE_LIST.append(device)

        device._description = description
        device._device_type = DeviceType(**device_type_dict)
        device._modules = DeviceModule.resolve_modules(module_names)
        device._attributes = DeviceAttribute.generate_deviceattribute_list(attribute_dict)

        return device

