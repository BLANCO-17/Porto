import fetch from 'node-fetch';

function ct(){

  let params = {
    "name": "BTC",
    "CUR": "INR",
    "cost": "1700",
    "shares": "5",
    "user": "test"
  };
  
  let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
  
  let url = "http://127.0.0.1:5000/createTrade?"+query
  
  fetch(url)
  .then(data => data.text())
  .then( (text) => {
    console.log(text) 
     //do something awesome that makes the world a better place
  });
}

function getTrade(){
  let params = {
    "name": "BTC",
    "user": "test"
  };

  let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');

  let url = "http://127.0.0.1:5000/getTrade?"+query;

  fetch(url)
  .then(data => data.text())
  .then((data) => {
    console.log(data.name);
  });
  
}

getTrade()