from webserver.webserver import Webserver
import logging


log = logging.getLogger("Webserver")


def start():
    log.info("Start flask webserver")
    web = Webserver(name="Webserver")
    web.start()


if __name__ == "__main__":
    start()