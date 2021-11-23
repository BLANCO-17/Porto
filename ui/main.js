const { app, ipcMain } = require('electron');
const { BrowserWindow, setVibrancy} = require("electron-acrylic-window");


let win;
let item_win_on = false;
let add_item_win;

function createWindow () {
    win = new BrowserWindow({
        minWidth: 550,
        minHeight: 720,
        title: "Porto",        
        frame: false,
        transparent: true,      
        webPreferences: {nodeIntegration: true, contextIsolation: false,  enableRemoteModule: true}  
    })
    win.setSize(1000, 600)
    win.loadFile('index.html')
    // win.webContents.openDevTools();
    // uncommment above statement for console/debug access in app    

    op = {
        theme: 'dark',
        effect: 'blur',
        useCustomWindowRefreshMethod: true,
        maximumRefreshRate: 60,
        disableOnBlur: false
     };
    win.setVibrancy(op);

    ipcMain.on('minimize', () => {
        win.minimize()        
    });
    ipcMain.on('maximize', () => {
        win.isMaximized() ? win.unmaximize() : win.maximize()
    });
    ipcMain.on('close-window', () => {
        win.close()        
        app.quit()
    });
};

app.whenReady().then(() => {
    createWindow()
});

