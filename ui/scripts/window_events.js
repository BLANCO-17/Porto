const { ipcRenderer } = require("electron");

function closeWindow(){    

    const param = {"cmd": "quit"};    
    
    let url = "http://127.0.0.1:5000/systemcmds?cmd=quit"

    fetch(url)
    .then(data => data.json())
    .then((data)=>console.log(data));
    
    ipcRenderer.send('close-window');

}

function MinWindow(){
    ipcRenderer.send('minimize');
}

function MaxWindow(){
    ipcRenderer.send('maximize');
}

// function OpenItemWindow(){
//     ipcRenderer.send('create-add-window');
// }
// function CloseItemWindow(){
//     ipcRenderer.send('close-add-window');    
// }