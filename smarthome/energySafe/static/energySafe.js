var device_names = [
    "apu-board",
    "security-gateway",
    "workstation",
    "storage-one",
    "storage-two",
    "accesspoint"
];


function addDivider(onlyGet=false){
    let el = document.createElement("li");
    el.className = "table-view-divider";
    if(!onlyGet){
        id("event-list").prepend(el);
    }
    return el;
}

function addCell(name, onlyGet=false){
    let el = document.createElement("li");
    el.className = "table-view-cell";
    el.innerHTML = name+"<div class='loader right'></div>";
    el.setAttribute("data-device-name", name);
    if(!onlyGet){
        id("event-list").prepend(el);
    }
    return el;
}

function modifyCell(element, action, state){
    let name = element.getAttribute("data-device-name");
    let html = name+" - "+action;
    if(state == "loading"){
        html += "<span class='loader right'></span>";
    }else{
        html += "<span class='right'>"+state+"</span>";
    }
    element.innerHTML = html;
}

function id(name){
    return document.getElementById(name)
}


function poweroff(device_name){

    let ele = addCell(device_name);
    modifyCell(ele, "poweroff", "loading");
    fetch("/api/poweroff/"+device_name)
        .then( (response) => { return response.json() })
        .then( (json) => {

            modifyCell(ele, "poweroff", "send");

            ele.addEventListener("click", function(){
                alert(JSON.stringify(json, null, 2));
            });
        });
}
function secondsToTime(secs)
{
    secs = Math.round(secs);
    var hours = Math.floor(secs / (60 * 60));

    var divisor_for_minutes = secs % (60 * 60);
    var minutes = Math.floor(divisor_for_minutes / 60);

    var divisor_for_seconds = divisor_for_minutes % 60;
    var seconds = Math.ceil(divisor_for_seconds);

    var obj = {
        "h": hours,
        "m": minutes,
        "s": seconds
    };
    return obj.h+"h "+ obj.m+"m "+obj.s+"s";
}

function wait(device_name, new_state, timeout, maincallback){
    let start = new Date();

    let element_list = [];
    let request_chain = [];
    let device_list = [];
    if(typeof device_name == "string"){
        device_list.push(device_name)
    }else{
        device_list = device_name
    }

        device_list.forEach( (device_name) => {
            let ele = addCell(device_name);
            modifyCell(ele, "wait", "loading");
            element_list[device_name] = ele;
            request_chain.push( (pcallback) => {
                checkRequest(device_name, pcallback);
            });
        });

    retest();
    function retest(){
        async.parallel(request_chain, (err, results)=>{
            let endresult = true;
            results.forEach( (item) => {
                if( item !== new_state){
                    endresult = false;
                }
            });

            if(endresult){
                maincallback();
            }else{
                if((new Date() - start)/1000 > timeout){
                    alert("TIMEOUT after" + (new Date() - start)/1000);
                    element_list.forEach( (item, name) => {
                        modifyCell(item, "wait", "failed");
                    });
                }else{
                    for ( var index in element_list){
                        modifyCell(element_list[index], "wait", "loading");
                    }
                    window.setTimeout( () => {
                        retest();
                        console.log("Trigger rewait");
                    }, 2000);
                }
            }
        });
    }

    async function checkRequest(device_name, parallelcallback) {
        await fetch("/api/status/" + device_name)
            .then((response) => {
                return response.json()
            })
            .then((json) => {
                var ele = element_list[device_name];
                modifyCell(ele, "wait", "processed");
                parallelcallback(null, json.device_status);
            });
    }
}

function status(device_name){
    let elem = addCell(device_name);
    modifyCell(elem, "status", "loading");
    fetch("/api/status/"+device_name)
        .then( (response) => { return response.json() })
        .then( (json ) => {
            modifyCell(elem, "status", json.device_status);
        });
}

function socketGetState(){
    fetch("/api/socket/getstate")
        .then( (response) => { return response.json() })
        .then( (json ) => {
            for ( let index in json.sockets) {
                let value = json.sockets[index];
                let elem = addCell(index);
                modifyCell(elem, "state",  value);
            }
        });
}

function socketGetEnergy(){
    fetch("/api/socket/getenergy")
        .then( (response) => { return response.json() })
        .then( (json ) => {
            for ( let index in json.sockets) {
                let value = json.sockets[index];
                let elem = addCell(index);
                modifyCell(elem, "energy",  value);
            }
        });
}

function wol(device_name){
    let elem = addCell(device_name);
    modifyCell(elem, "wol", "loading");
    fetch("/api/wol/"+device_name)
        .then( (response) => { return response.json() })
        .then( (json ) => {
            modifyCell(elem, "wol", "send");
        });
}


function display_state(state){
    let elem = addCell("Display");
    let state_text = "off";
    if(state){
        state_text = "on"
    }

    modifyCell(elem, "", "loading");

    fetch("/api/monitor/"+state_text)
    .then( (response) => { return response.json() })
    .then( (json ) => {
        modifyCell(elem, "",  state_text);
    });

}

function socket_state_by_name(state, names){
    let name_str = names.join("-")
    if(state){
        endpoint = "on"
    }else{
        endpoint = "off"
    }

    fetch("/api/socket/"+name_str+"/state/"+endpoint)
    .then( (response) => { return response.json() })
    .then( (json ) => {

        for(let i in json.affected){
            let elem = addCell("Power Socket")
            modifyCell(elem, json.affected[i], endpoint);
        }
    });
}

function popoverClose(){
    document.querySelector(".backdrop").remove();
    document.getElementById("popover").classList.remove("visible");

}

document.getElementById("action-stop-all").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Stop all";

    poweroff("workstation");
    display_state(false);
    wait("workstation", false, 180, () =>{
        poweroff("storage-two");
        poweroff("storage-one");
        poweroff("usg");
        poweroff("ap");

        wait(["storage-two", "storage-one"], false, 180, () => {
            poweroff("apu");

            wait("apu", false, 120, () => {

                let energy_elem = addCell("Energy");
                let energy_timer = window.setInterval(function(){

                    fetch("/api/socket/getenergy")
                        .then( (response) => { return response.json()})
                        .then( (json) => {
                            if(json.status == "ok"){
                                modifyCell(energy_elem, "monitor", json.sockets["Infrastruktur"]);
                                if( json.sockets["Infrastruktur"] <= 40.0 ){
                                    window.clearInterval(energy_timer);
                                    poweroff_timer();
                                }
                            }else{
                                modifyCell(energy_elem, "monitor", "error");
                            }
                        })
                }, 3000);

                function poweroff_timer(){
                    let waittime = 30;
                    let startdate = new Date();
                    let socket_off_info = addCell("<b>FullPowerOff</b>");
                    let socket_off_timer = window.setInterval(() => {
                        let countdown = waittime - ((new Date() - startdate)/1000);
                        modifyCell(socket_off_info, "", secondsToTime(Math.round(countdown)));
                        if(countdown <= 0){
                            socket_state_by_name(false, ["infrastruktur", "multimedia", "pc"])
                            window.clearInterval(socket_off_timer);
                        }
                    }, 1000);
                }
            });
        });
    });
});

document.getElementById("action-status-all").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Display Status";

    device_names.forEach( (item) => {
        status(item);
    });
    socketGetEnergy();
    socketGetState();
});

document.getElementById("action-start-all").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Start all";
    socket_state_by_name(true, ["pc", "multimedia", "infrastruktur"])

    wait("apu", true, 300, () => {
        wol("storage-one");
        wol("storage-two");

        wait(["apu", "storage-one", "storage-two"], true, () => {
            wol("workstation");
            display_state(true);
        });
    });
});

document.getElementById("action-display-on").addEventListener("click", function(){
    popoverClose();
    display_state(true);
});

document.getElementById("action-display-off").addEventListener("click", function(){
    popoverClose();
    display_state(false);
});

document.getElementById("action-stop-except-internet").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Stop all except Internet";

    poweroff("workstation");

    wait("workstation", false, 180, () =>{
        poweroff("storage-two");
        poweroff("storage-one");

        wait(["storage-two", "storage-one"], false, 180, () => {
            poweroff("apu");
            socket_state_by_name(false, ["pc", "multimedia"]);
        });
    });
});

document.getElementById("action-media-on").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Start Mulitmedia";

    socket_state_by_name(true, ["multimedia"])
});

document.getElementById("action-workday-start").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Good Morning";
    socket_state_by_name(true, ["pc", "infrastruktur"])

    wait("apu", true, 300, () => {
        wol("storage-one");
        wol("storage-two");

        wait(["apu", "storage-one", "storage-two"], true, () => {
            wol("workstation");
            display_state(true);
        });
    });
});

document.getElementById("action-workstation-on").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Start Workstation";
    socket_state_by_name(true, ["pc"])
    wol("workstation");
    display_state(true);
});

document.getElementById("action-workstation-off").addEventListener("click", function(){
    popoverClose();
    addDivider().innerHTML = "Stop Workstation";
    poweroff("workstation");
    wait("workstation", false, 300, function(){
        display_state(false);
        socket_state_by_name(false, ["pc"])
    })
});
