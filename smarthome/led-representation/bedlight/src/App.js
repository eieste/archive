import React, { useState } from 'react';
import { render } from "react-dom";
import ColorBar, {drawStart} from "./components/colorbar/colorbar.js"
import { Stage, Layer, Rect, Text } from "react-konva";
import { SketchPicker, TwitterPicker } from 'react-color'
import BedSkeleton from './bedskeleton';


function App() {

  const [color, setColor] = useState({"hex":"#000000"});
  const [colorBar, setColorBar] = useState([]);
  
  function onMouseMove(event){
    drawStart(color, colorBar, setColorBar, event);
  }

  return (
    <div>
      <Stage width={window.innerWidth} height={100} onMouseMove={onMouseMove.bind(this)}>
        <ColorBar color={color} colorBar={colorBar} />
      </Stage>
      <TwitterPicker onChange={setColor} />
    </div>
  );
}

export default App;