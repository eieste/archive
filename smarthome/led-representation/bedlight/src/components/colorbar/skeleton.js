import React, { Component } from "react";
import Konva from "konva";
import { render } from "react-dom";
import { Stage, Layer, Rect, Text } from "react-konva";
import settings from "./settings.js";
import Paho from "paho-mqtt";


class ColorBarSkeleton extends React.Component {
  
  constructor(props) {
    super(props);
    let self = this;
    self.skeleton = {
      x: 20,
      y: 20,
      width: window.innerWidth-50,
      height: 50
    }
  }

  render() {
    let self = this;
    return (

        <Rect
            x={self.skeleton.x}
            y={self.skeleton.y}
            width={self.skeleton.width}
            height={self.skeleton.height}
            stroke={'black'}
            strokeWidth={1}
        />
    );
  }
}

export default ColorBarSkeleton;


















































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