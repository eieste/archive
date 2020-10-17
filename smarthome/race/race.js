const prefix = "@flatos/bedlight/";

var player = {
    "color": "0,0,0",
    "name": "unknown",
    "lap": 0
}

var playerList = [];

var client = null;

window.addEventListener('load', function () {
    client = new Paho.Client("controller.flatos", 1884, "myClientId" + new Date().getTime());
    client.onMessageArrived = onMessageArrived;
    client.connect({onSuccess:onConnect});
});
  
  

function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe(prefix+"race/welcome/player");
  client.subscribe(prefix+"race/ready");
  client.subscribe(prefix+"race/countdown");
  client.subscribe(prefix+"race/race");
  //message = new Paho.MQTT.Message("Hello");
  //message.destinationName = "World";
  //client.send(message);
}

// called when a message arrives
function onMessageArrived(message) {
    console.log(message);
    try{    
        if(message.destinationName == prefix+"race/welcome/player"){
            playerList = JSON.parse(message.payloadString).playerList;
            writeCurrentPlayerList(playerList);
            console.log(playerList);
        }

        if(message.destinationName == prefix+"race/ready"){
            if(message.payloadString != player.name){
                document.getElementById("ready_start").remove();
                document.getElementById("ready_master").innerHTML = message.payloadString;
            } else{
                window.setTimeout(function(){
                    let message = new Paho.Message("start");
                    message.destinationName = prefix+"race/countdown";
                    client.send(message);

                    message = new Paho.Message(new Uint8Array([0,0,0,0,158]));
                    message.destinationName = prefix+"led/color";
                    client.send(message);
                }, 1000)

            }
        }

        if(message.destinationName == prefix+"race/countdown"){
            if(message.payloadString == "start"){
                document.getElementById("ready_screen").remove();
                document.getElementById("countdown_screen").style.display="block";    
                let start = 5;
                let ctn = window.setInterval(function(){
                    document.getElementById("countdown").innerHTML = start;
                    start--;
                    if (start <= 0){
                        window.clearInterval(ctn);
                        document.getElementById("countdown_screen").remove();
                        document.getElementById("raceGameScreen").style.display = "block";
                        startGame();
                    }
                }, 1000)
            }
        }

        if(message.destinationName == prefix+"race/race"){
            let data = JSON.stringify(message.payloadString);
            playerList.forEach(function(item){
                if(item.name == data.name){
                    item["lap"] = data.lap;
                }
            })
            writeCurrentPlayerList(playerList);
        }


    } catch(e){
        console.error(e);
    }
}

document.getElementById("welcome_start").addEventListener("click", function(){
    let playername = document.getElementById("welcome_playername").value;
    let playercolor = document.getElementById("welcome_playercolor").value;

    player = {
        "name": playername,
        "color": playercolor
    };
    
    let message = new Paho.Message(JSON.stringify({
        "playerList": [
            ...playerList, 
            player
        ]
    }));

    message.destinationName = prefix+"race/welcome/player";
    client.send(message);
    document.getElementById("welcome_screen").remove();
    
    document.getElementById("ready_screen").style.display="block";
});

document.getElementById("ready_start").addEventListener("click", function(){

    let message = new Paho.Message(player.name);
    message.destinationName = prefix+"race/ready";
    client.send(message);

});



function writeCurrentPlayerList(player_list){
    let ul = document.createElement("ul");

    player_list.forEach(function(item){

        let li = document.createElement("li");

        let data =  item.name+" ("+item.color+")";
        if(item.hasOwnProperty("lap")){
            data = data + "<b>"+item.lap+"</b>";
        }
        li.innerHTML = data;
        ul.append(li);
    });

    let elem_list = document.getElementsByClassName("currentPlayerList");
    
    for(let i = 0; i < elem_list.length; i++){
        let el = elem_list[i];
        el.innerHTML = ul.outerHTML;
    }
}


function startGame(){
    let count = 0;
    let color = player.color.split(",");
    for(var i=0; i<color.length;i++) color[i] = parseInt(color[i]);

    document.getElementById("raceGameScreen").addEventListener("click", function(){
        let ar = [...color, count, count+1];
        let data = new Uint8Array(ar)
        let message = new Paho.Message(data.buffer);
        message.destinationName = prefix+"led/color";
        client.send(message);

        message = new Paho.Message(new Uint8Array([0,0,0,count-1, count]));
        message.destinationName = prefix+"led/color";
        client.send(message);



        if(count >= 157){
            count = 0;
            player.lap = parseInt(player.lap)++;
            document.getElementById("lap").innerHTML = player.lap;
            let message = new Paho.Message(JSON.stringify(player));
            message.destinationName = prefix+"race/race";
            client.send(message);

            message = new Paho.Message(new Uint8Array([0,0,0,157,158]));
            message.destinationName = prefix+"led/color";
            client.send(message);

        }

        count++;

    });


}
