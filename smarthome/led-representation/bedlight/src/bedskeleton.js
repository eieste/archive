import React, { Component } from "react";
import Konva from "konva";
import { render } from "react-dom";
import { Stage, Layer, Rect, Text } from "react-konva";
import settings from "./settings.js";
import Paho from "paho-mqtt";


class BedSkeleton extends React.Component {
  
  constructor(props) {
    super(props);
    let self = this;
    self.skeleton = {
      x: 20,
      y: 20,
      width: window.innerWidth-50,
      height: 50
    }
    self.setColorBarItem = props.setColorBarItem
    self.factor =  settings.LED_COUNT / ( (self.skeleton.x+self.skeleton.width) - self.skeleton.x);

  }

  state = {
    color: {"rgb": {"r":0, "g":0, "b":0}},
    colorlist: []
  };
  componentWillReceiveProps(props){
    let self = this;
    self.setState({"color": props.color})
  }

  drawStart(event){
    let self = this;
    let cursorX = event.evt.layerX;
    
    let px = (cursorX-self.skeleton.x) * self.factor;

    let colorset = self.state.colorlist;
    colorset[Math.round(px)] = self.state.color;
    self.setState({"colorlist": colorset});

      let b =[self.state.color.rgb.r, self.state.color.rgb.g, self.state.color.rgb.b]
      let ar = [...b, px, px+1];
      let data = new Uint8Array(ar)
      let message = new Paho.Message(data.buffer);
      message.destinationName = "@flatos/bedlight/led/color";
      settings.MQTT.send(message);
  }


  render() {
    let self = this;
    return (<Rect
        onMouseMove={self.drawStart.bind(self)}
        x={self.skeleton.x}
        y={self.skeleton.y}
        width={self.skeleton.width}
        height={self.skeleton.height}
        stroke={'black'}
        strokeWidth={1}
      />);
  }
}

export default BedSkeleton;