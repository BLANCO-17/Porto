const { ipcRenderer } = require("electron");

function closeWindow(){    
    ipcRenderer.send('close-window');
}

function MinWindow(){
    ipcRenderer.send('minimize');
}

function MaxWindow(){
    ipcRenderer.send('maximize');
}

