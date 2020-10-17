#!/bin/bash


echo "Upload"
mpfshell -n -c "open ttyUSB0;
                md contrib;
                md control;
                md power;
                put contrib/broadlink.py;
                put contrib/wifi.py;
                put contrib/WS2801.py;
                put power/main.py;
                put power/power_monitor.py;
                put main.py;
                put settings.py;
                put control/control_manager.py;
                put control/control_server.py;
                put control/control_parameters.py;
                put control/main.py"