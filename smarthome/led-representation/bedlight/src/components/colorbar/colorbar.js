import React, { Component } from "react";
import Konva from "konva";
import { render } from "react-dom";
import { Stage, Layer, Rect, Text } from "react-konva";
import settings from "../../settings.js";
import Paho from "paho-mqtt";


const skeleton ={
    x: 20,
    y: 20,
    width: window.innerWidth-50,
    height: 50}

const factor = settings.LED_COUNT / ( (skeleton.x+skeleton.width) - skeleton.x);


class ColorBar extends React.Component {
  
  constructor(props) {
    super(props);
    let self = this;
  }

  state = {
    color: {"rgb": {"r":0, "g":0, "b":0}},
    colorlist: []
  };

  componentWillReceiveProps(props){
    let self = this;
    console.log(props);
    self.setState({"color": props.color});
    self.setState({"colorlist": props.colorBar});
  }


  render() {
    let self = this;
    return [

            <Layer>

                <Rect
                    x={skeleton.x}
                    y={skeleton.y}
                    width={skeleton.width}
                    height={skeleton.height}
                    stroke={'black'}
                    strokeWidth={1}
                />
            </Layer>
            ,
            <Layer>
                {
                    ((()=>{
                
                        let self = this;
                        let result = [];
                            
                        self.state.colorlist.forEach(function(item, index){

                          console.log(index, item, (((1/factor)*index)+(1/factor)), skeleton.y);
                            let a = <Rect
                                x={((1/factor)*index)+(1/factor)}
                                y={skeleton.y}
                                width={1/factor}
                                height={skeleton.height}
                                fill={item.hex}
                            />;
                            result.push(a);
                        })
                        return result;
                    })())
                }
            </Layer>
        ]
    }
}

export default ColorBar;

function drawStart(color, colorBar, setColorBar, event) {
    let cursorX = event.evt.layerX;

    let px = (cursorX-skeleton.x) * factor;

    let colorset = colorBar;
    colorset[Math.round(px)] = color;

    setColorBar(colorset);

    let b =[color.rgb.r, color.rgb.g, color.rgb.b]
    let ar = [...b, px, px+1];
    let data = new Uint8Array(ar)
    let message = new Paho.Message(data.buffer);
    message.destinationName = "@flatos/bedroom/bedlight/led/color";
    settings.MQTT.send(message);
}

export {
    drawStart
}


/*
export default function(){
    


    <Layer>
    <BedSkeleton setColorBarItem={setColorBarItem} color={color}/>
  </Layer>
  <Layer>
    {
            ((()=>{
      
              let self = this;
              let result = [];
                
              colorBarItem.forEach(function(item, index){
                  let a = <Rect
                    x={((1/self.factor)*index)+(1/self.factor)}
                    y={self.skeleton.y}
                    width={1/self.factor}
                    height={self.skeleton.height}
                    fill={item.hex}
                  />;
                  self.colorbar.appendChild(a);
                  //result.push(a);
              })
              return result;
            })())
    }
  </Layer>


}
*/