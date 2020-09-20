from flask import Flask, redirect, Response, render_template
import json
from collections import namedtuple
from controller import *
import traceback
import logging
import paramiko.ssh_exception

log = logging.getLogger("energySafe")
log.setLevel(logging.DEBUG)

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates')

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status/<name>")
def api_status(name):
    dev = find_device(name)
    return json.dumps({
        "status": "ok",
        "device_status": is_open(dev.ip, 22, 5)
    })

@app.route("/api/poweroff/<name>")
def api_poweroff(name):
    dev = find_device(name)
    try:
        result = poweroff(dev)
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        return Response(json.dumps({
            "status": "ok",
            "message": "already-off"
        }), mimetype="application/json")

    except Exception as e:
        log.debug(result)
        log.exception(e)
        return Response(json.dumps({
            "status": "error",
            "exception": str(e),
            "traceback": traceback.format_exc()
        }), mimetype="application/json")

    return Response(json.dumps({
        "status": "ok",
        "stdout": result[0],
        "stderr": result[1]
    }), mimetype="application/json")

@app.route("/api/wol/<name>")
def api_wol(name):
    dev = find_device(name)
    try:
        result = remote_wol(dev)
    except Exception as e:
        log.exception(e)
        return Response(json.dumps({
            "status": "error",
            "exception": str(e),
            "traceback": traceback.format_exc()
        }), mimetype="application/json")
    return Response(json.dumps({
        "status": "ok",
        "stdout": result[0],
        "stderr": result[1]
    }), mimetype="application/json")

@app.route("/api/monitor/<sockets>/state/<state>")
def api_monitor_socket(sockets, state):
    socket_names = sockets.split("-")

    for i in socket_names:
        if i in [1,2,3,4, "1", "2", "3", "4"]:
            if state.lower() in ["true", "on"]:
                os.system("sispmctl -o {}".format(i))
            else:
                os.system("sispmctl -f {}".format(i))

    return json.dumps({
        "status": "ok"
    })


@app.route("/api/socket/<sockets>/state/<state>")
def api_socket_setstate_by_name(sockets, state):
    socket_names = sockets.split("-")

    socket_list = find_sockets_by_names(socket_names)

    if state.lower() in ["true", "on"]:
        socket_set_state(socket_list, True)
    else:
        socket_set_state(socket_list, False)

    return json.dumps({
        "status": "ok",
        "affected": [ n.name for n in socket_list]
    })


@app.route("/api/socket/setstate/<state>")
def api_socket_setstate(state):
    if state.lower() in ["true", "on"]:
        socket_set_state(SOCKET_LIST, True)
    else:
        socket_set_state(SOCKET_LIST, False)

    return json.dumps({
        "status": "ok",
    })

@app.route("/api/socket/getstate")
def api_socket_getstate():
    return Response(json.dumps({
        "status": "ok",
        "sockets": socket_get_state(SOCKET_LIST)
    }), mimetype="application/json")


@app.route("/api/socket/getenergy")
def api_socket_getenergy():
    try:
        return Response(json.dumps({
            "status": "ok",
            "sockets": socket_get_energy(SOCKET_LIST)
        }), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({
            "status": "error",
            "exception": str(e),
            "traceback": traceback.format_exc()
        }), mimetype="application/json")


if __name__ == '__main__':
    app.run("0.0.0.0", 80, debug=True)