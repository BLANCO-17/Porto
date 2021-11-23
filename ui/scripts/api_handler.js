var fs = require ('fs');
let all_items = [];


function getUserData(){    

    // let params = {        
    //     "user": "user",
    //     // "psd": "test123"
    // };

    // let query = Object.keys(params)
    //                .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
    //                .join('&');
    
    // let url = "http://127.0.0.1:5000/getUserItems?"+query;

    // fetch(url)
    // .then(data => data.text())
    // .then((data) => {
    //     data = JSON.parse(data);
    //     console.log(data.items);
    //     createElements(data.items);        
    // });
}

function setItemDetails(item, data_list){    
  document.getElementById(item.toLowerCase()+"_cost").textContent = "SPENT : "+data_list[item].cost;
  document.getElementById(item.toLowerCase()+"_qty").textContent = "SHARES : "+data_list[item].shares;

  let params = {        
    "item": item
      // "psd": "test123"
  };

  let query = Object.keys(params)
                .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                .join('&');
    
  let url = "http://127.0.0.1:5000/getTrade?"+query;

  fetch(url)
  .then(data => data.text())
  .then(async(data)=>{
    data = JSON.parse(data);   
    var totalcost=0;
    var qty=0;
    var itemprice = await getItemPrice(item);
    itemprice = Number(itemprice).toFixed(2);
    var TotalValueBPerTrade=0;
    // console.log(data)
    for(var key in data){
      if(data.hasOwnProperty(key)){
          qty += shares = Number(data[key].shares);
          cost = Number((data[key].cost) * shares);
          totalcost += cost;
          TotalValueBPerTrade += (itemprice*shares)-cost;
          // console.log(item, shares, cost)
        }
      }
    TotalValueBPerTrade = Number(TotalValueBPerTrade).toFixed(2)

    var PL = document.getElementById(item.toLowerCase()+"_PL");
    var hodl = document.getElementById(item.toLowerCase()+"_tradeHodl");
    PL.textContent = TotalValueBPerTrade;
    hodl.textContent = "HODL VALUE : "+Number(qty*itemprice).toFixed(2);

    if(TotalValueBPerTrade < 0)
      PL.style.color = "red";
    else
      PL.style.color = "limegreen";

  });
}

var createElements = function(items, currency=""){
    var container = document.getElementById('port_con');
    all_items = [];
    document.getElementById('items_bar').innerHTML = "";
    items.forEach(async (element) => {

        var items_data = [];
        all_items.push(element.toLowerCase());
        // console.log(all_items)
        var ele = document.createElement('div');
        
        var code = `
                      <div class="tradecard" id="${element}_card">
                        <div style="display: block; float:left; width: 75%;">
                          <span class="carditem" id=${element.toLowerCase()}_itemname >${element}</span>
                          <span class="underline">${element}/INR</span>
                          <div class="itemVal" id="${element.toLowerCase()}_itemValParent">
                            <span class="itemPrice" id="${element.toLowerCase()}_itemVal"> </span>
                            <span class="pcLogo">⥮</span>
                            <span class="itemPChange" id="${element.toLowerCase()}_tradePC">1</span>
                          </div>                          
                          <span class=tradeqty id="${element.toLowerCase()}_qty">SHARES : 0 </span>                                                    
                          <span class=tradeHold id="${element.toLowerCase()}_tradeHodl">HODL VALUE : </span>
                          <div class="tots">
                            <span class=totalcost id="${element.toLowerCase()}_cost">SPENT : 0 </span>
                            <div class=totalValCon>
                              <span>PROFIT/LOSS : </span>                  
                              <span id="${element.toLowerCase()}_PL"></span>
                            </div>                                                        
                          </div>
                        </div>
                        <div style="float: right; width:25%; height:50%;">
                          <img class="itemlogo" src="https://cryptoicon-api.vercel.app/api/icon/${element.toLowerCase()}" alt="">
                        </div>
                      </div>
                  `;
        // console.log(element.toLowerCase())
        ele.innerHTML = code;
        container.appendChild(ele);
        let x = await getItemData(element);
        items_data[element] = JSON.parse(x);
        
        setItemDetails(element, items_data);
        setupTradePage_items(element.toLowerCase());
        // set_Item_trades(element);
        // console.log(items_data)
    });
}

function refreshItemPrice(){
  
    
  all_items.forEach(element => {

    // let url = "https://api.coinbase.com/v2/prices/"+element+"-USD/buy";
    let url = "https://api.wazirx.com/sapi/v1/trades?symbol="+element.toLowerCase()+"usdt&limit=1"
    // let url = "https://api.nomics.com/v1/currencies/ticker?key=6cef157eb2943ba698ad3453385dcfd7e94c2e31&ids="+element+"&convert=USD";
    fetch(url)
    .then(data => data.text())
    .then((data) => {
      data = JSON.parse(data)['0'];
      // console.log(data);
      document.getElementById(element+'_itemVal').textContent = data.price;      
    });

    let p_url = "https://coincodex.com/api/coincodex/get_coin/"+element;
    fetch(p_url)
    .then(data => data.text())
    .then((data) => {
      data = JSON.parse(data);
      var pc = Number(data.price_change_1D_percent).toFixed(2);
      document.getElementById(element.toLowerCase()+"_tradePC").textContent = pc;
      document.getElementById(element.toLowerCase()+"_itemname").textContent = data.coin_name;
      if(pc < 0)
      {
        document.getElementById(element+"_itemValParent").style.color = "red";
      }else{
        document.getElementById(element+"_itemValParent").style.color = "limegreen";
      }            
      // console.log(Number(data.price_change_1D_percent).toFixed(2));
    });
    
  });
}

async function getItemData(item){

  let params = {        
    "item": item
      // "psd": "test123"
  };

  let query = Object.keys(params)
                .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                .join('&');

  let url = "http://127.0.0.1:5000/getDetails?"+query;

  const output = await fetch(url)
  .then(data => data.text())
  .then((data)=> {
    // var x = JSON.parse(data);
    return data; //JSON.stringify(x);
  });
  return output;
}

function setupTradePage_items(item){
  var items_bar = document.getElementById('items_bar');
  // items_bar.innerHTML = "";
  
  let newItem = document.createElement('div');    
  let code =`
              <img class="itemicon itemicon_overlay" src="https://cryptoicon-api.vercel.app/api/icon/${item}" id="${item}_itembtn">
            `;
  newItem.innerHTML = code;

  items_bar.appendChild(newItem);
}

async function getItemPrice(item){
  // let url = "https://api.coinbase.com/v2/prices/"+item.toLowerCase()+"-USD/buy";    
  let url = "https://api.wazirx.com/sapi/v1/trades?symbol="+item.toLowerCase()+"usdt&limit=1"
  let price = await fetch(url)
    .then(data => data.text())
    .then((data) => {
      data = JSON.parse(data)['0'];
      // console.log(data);
      return Number(data.price).toFixed(2);
    });
  return price;
}

function set_Item_trades(item){
  
}

// item, cur, qty, buyprice
function add_new_item(){

  let item = document.getElementById('item_select').textContent;
  let cur = document.getElementById('cur_select').textContent;
  let qty = Number(document.getElementById('item_qty').value).toFixed(3);
  let buyprice = Number(document.getElementById('item_price').value).toFixed(2);

  let params = {
    "name": item,
    "CUR": cur,
    "cost": buyprice,
    "shares": qty
  };

  let query = Object.keys(params)
                .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                .join('&');

  let url = "http://127.0.0.1:5000/createTrade?"+query;
  
  // console.log(item, cur, qty, buyprice);  

  fetch(url)
  .then(data => data.text())
  .then((data)=>{
    data = JSON.parse(data);
    // console.log(data.output.name);
    // createElements([data.output.name], data.output.CUR);

    // if(all_items.includes(data.output.name) == false)
    //   all_items.push(data.output.name);
    refreshApp();
  });
  
  
}

function refreshApp(){
    
  let params = {        
    "user": "user"    
  };

  let query = Object.keys(params)
                 .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                 .join('&');
  
  let url = "http://127.0.0.1:5000/getUserItems?"+query;

  fetch(url)
  .then(data => data.text())
  .then((data) => {
      data = JSON.parse(data);
      var port = document.getElementById('port_con');
      port.innerHTML = "";
      createElements(data.items);
  });
  
}

const ref = setInterval(refreshItemPrice, 3000);
// const refa = setInterval(refreshApp, 3000);

// window.onload = function(){getUserData();}
// getUserData();
refreshApp();
