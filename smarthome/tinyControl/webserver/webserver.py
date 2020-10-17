import threading
import logging

log = logging.getLogger("Webserver")
log.setLevel(logging.DEBUG)


class Webserver(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Webserver, self).__init__(*args, **kwargs)

    def run(self):
        app.run("0.0.0.0", 80, debug=True)
        pass