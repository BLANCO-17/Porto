let add_item_enabled = false;
let port_visible=true;
let trade_visible=false;

function displayPort(){
    if(!port_visible){
        trade_visible = false;
        port_visible = true;

        document.getElementById('trade_con').style.opacity = 0;
        document.getElementById('trade_con').style.visibility = 'hidden';
        document.getElementById('trade_con').classList.toggle('active');
        setTimeout(function(){
        document.getElementById('port_con').style.opacity = 1;
        document.getElementById('port_con').style.visibility = 'visible';
        document.getElementById('port_con').classList.toggle('active');
        }, 500);
    }
}

function displayTrades(){
    if(!trade_visible){
        trade_visible = true;
        port_visible = false;

        document.getElementById('port_con').style.opacity = 0;
        document.getElementById('port_con').style.visibility = 'hidden';
        document.getElementById('port_con').classList.toggle('active');    
        setTimeout(function(){
            document.getElementById('trade_con').style.visibility = 'visible';
            document.getElementById('trade_con').style.opacity = 1;
            document.getElementById('trade_con').classList.toggle('active');
        }, 500);
    }
}

function toggle_sidebar(){
    document.getElementById('sdb').classList.toggle('active');
    var sidetext = document.getElementsByClassName('text');

    for(var i=0; i<sidetext.length; i++){
        sidetext[i].classList.toggle('active');
    }
}

function toggle_dropdown(item){
    document.getElementById(item).classList.toggle('active');
}

function ToggleItemWindow(){

    var add_window = document.getElementById('add_item_window');
    var main_window = document.getElementById('mainwindow');
    
    if(!add_item_enabled)
    {
        add_item_enabled = true;
        add_window.style.visibility = "visible";        
        main_window.style.zIndex = -10;
        add_window.style.opacity = 1;        
        add_window.classList.toggle('active');
    }
    else
    {
        add_window.classList.toggle('active');
        add_window.style.opacity = 0;
        setTimeout(function(){
            add_item_enabled = false;
            add_window.style.visibility = "hidden";    
            main_window.style.zIndex = 10;
        }, 1000);
    }
}

window.onload = function(){
    var dditems = document.getElementsByClassName('dditem');

            for(var i=0; i<dditems.length; i++)
            {
                let item = dditems[i];

                if(item.parentElement.id == 'item_select_list')
                {
                    item.onclick = function(){
                        //console.log(item.textContent);                    
                        document.getElementById('item_select').value = item.textContent;
                    }
                }else{
                    item.onclick = function(){
                        //console.log(item.textContent);                    
                        document.getElementById('cur_select').textContent = item.textContent;
                    }
                }
            }
}
