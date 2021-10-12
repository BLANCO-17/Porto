const fs = require('fs');
const { stringify } = require('querystring');

const btcfunc = setInterval(function(){ 
    url = "https://api.coinbase.com/v2/prices/BTC-USD/buy"
    fetch(url)
    .then(data => data.json())
    .then((data) => {
        // data=JSON.parse(data)
        // console.log(data.data.amount)
        try {
            document.getElementById("btc_itemVal").textContent = data.data.amount;
        } catch (error) {
            console.log(error)
        }
    });    
}, 5000);

function onStart(){
    
    fs.readFile('../data/test/log.dat', (err, data) => {
        if (err) throw err;  
        data = JSON.parse(data)
        console.log(data)
        document.getElementById('name_ele').textContent = data["user"];
    })

    let params = {
        "item": "BTC",
        "user": "test"
      };
    
      let query = Object.keys(params)
                   .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                   .join('&');
    
      let url = "http://127.0.0.1:5000/getTrade?"+query;
    
      fetch(url)
      .then(data => data.text())
      .then((data) => {
        data = JSON.parse(data);
        // console.log(data);
        var totalcost=0
        var qty=0
        var itemprice=42000
        var TotalValueBPerTrade=0

        for(var key in data){
            if(data.hasOwnProperty(key)){
                qty += shares = parseInt(data[key].shares)
                cost = parseInt((data[key].cost) * shares)
                totalcost += cost
                TotalValueBPerTrade += itemprice-cost

                // console.log(cost)
                // console.log(cost, shares)
            }
        }        
        
        let ele = document.createElement('div');        
        var html = `
                    <div class="tradecard" id=${data.item+'_card'}>
                        <div style="display: inline-flex; flex-flow:column; float:left; width: 75%;">
                            <span class=itemName id="itemName">Bitcoin</span>
                            <span class=underline id="itemAbv">BTC / USD</span>
                            <span class=itemval id="btc_itemVal">"Loading..." </span>
                            <span class=tradeval id="itemtradeVal">TRADE VALUE : ${TotalValueBPerTrade} </span>
                            <span class=tradeqty id="tradeQty">QUANTITY : ${qty} </span>
                        </div>
                        <div style="float: right; width:25%; height:50%;">
                            <span class=itemlogo> </span>
                        </div>
                    </div>
                    `
        ele.innerHTML = html;
        document.getElementById("container").appendChild(ele);
      });
    
}

onStart()

let btn = document.getElementById("menubtn");
let sidebar = document.getElementById("sbar");
let profile = document.getElementById("ptab");

btn.onclick = function(){
    profile.classList.toggle("active");
    document.querySelector(".dp").classList.toggle("active");
    document.querySelector(".userdata").classList.toggle("active");
    sidebar.classList.toggle("active");
};