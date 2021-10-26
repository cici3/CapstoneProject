let buttons = document.querySelectorAll('button');
let text_to_predict = document.getElementById('url');
let desc = document.getElementById('desc');

var head = document.getElementsByTagName('head')[0];
var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "http://code.jquery.com/jquery-2.2.1.min.js";

// Then bind the event to the callback function.
// There are several events for cross browser compatibility.
script.onreadystatechange = handler;
script.onload = handler;

// Fire the loading
head.appendChild(script);

function handler(){
   console.log('jquery added :)');
}

urlPing = "http://localhost:9999/ping"
urlPredict = "http://localhost:9999/predict_newscategory"

for (b of buttons) {
    b.addEventListener('click', (e) => {
        btext = e.target.innerText;
        switch (btext) {
            case 'CLASSIFY':
                console.log(url.value)
                desc.innerText = httpPostText();
                break;         
        }
    })
}
// function httpGet(theUrl) {
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open( "GET", theUrl ); 
//     console.log("response:", xmlHttp)
//     return xmlHttp.responseText;
// }

function convertJson(){
    //console.log(text_to_predict.value)
    var search_text = text_to_predict.value
    //console.log(search_text)
    var testString=  {"news_text":search_text}
    console.log(testString)
    return JSON.stringify(testString)
};
function httpPostText() {
    jQuery.ajax({
    type: 'POST',
    url: urlPredict,
    headers: {"Content-Type":"application/json"},
    data: convertJson(),
        success: function(msg) {
                console.log(msg);
                desc.innerText  =msg['news_category']
                desc.style.display = "block"
            },
        error: function(msg) {
            console.log(msg)
            //    alert('error: ' + msg)
             return false;
            },
    datatype: "json"

        });
}

function httpGet() {
    jQuery.ajax({
    type: 'GET',
    url: urlPing,    
    success: function(msg) {
            console.log(msg);
            desc.innerText = msg;
            },
    error: function() {
        alert('error');
        return false; }
        });
};



