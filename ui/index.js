const {app, BrowserWindow, ipcMain} = require('electron')

function createWindow(){
    const win = new BrowserWindow({
        title: "Porto",
        width: 800,
        height: 600,
        frame: false,
        transparent: true,      
        webPreferences: {nodeIntegration: true, contextIsolation: false,  enableRemoteModule: true}
        
    });
    win.loadFile('index.html');
    // win.webContents.openDevTools(); 

    ipcMain.on('minimize', () => {
        win.minimize()        
    });
    ipcMain.on('maximize', () => {
        win.isMaximized() ? win.unmaximize() : win.maximize()
    });
    ipcMain.on('close-window', () => {
        win.close()        
    });
};

app.whenReady().then(() => {
    createWindow();
});
