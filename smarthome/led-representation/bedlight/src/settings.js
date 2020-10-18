import Paho from "paho-mqtt";

const conf = {
    "LED_COUNT": 158,
    "MQTT": new Paho.Client("controller.flatos", 1884, "myClientId" + new Date().getTime())
 
}

conf.MQTT.connect({onSuccess:onConnect});

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
  }
  

export default conf

