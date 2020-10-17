import logging
from utils.conf import settings


log = logging.getLogger("plugin")


class BasePlugin:
    topic = None

    def on_message(self, topic, payload):
        raise NotImplemented("Please implement this method")
