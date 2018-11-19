var webSocket = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port);

webSocket.onopen = function () {
    //TODO iets verzinnen :)
};

webSocket.onclose = function () {
//    TODO proberen opnieuw verbinding te maken.
};

webSocket.onerror = function () {
//    TODO error handeling.
};

webSocket.onmessage = function (event) {
    //TODO error validation.
    console.log(event.data);
};

// function clamp(num, min, max) {
//     //  TODO documentatie beschrijving, weet nog steeds niet waar het handig voor is.
//     return num <= min ? min : num >= max ? max : num;
// }

$(".toggle").click(function () {
    $(this).toggleClass("active");
});

$(".buttonMic").click(function () {
    if($(this).hasClass("active")){
        // send enable
    }else{
        // send disable
    }
});

$("#screenText").on('blur', function () {
    var rovertext = $(this).val();
    var msg = {
        "key": "1234",
        "request": "displayMsg",
        "data": rovertext.toString()
    };
    webSocket.send(JSON.stringify(msg));
});


// videowebsocket

function videoWebsocketStart() {
    if ("WebSocket" in window) {
        var ws_path = 'ws://' + window.location.host + window.location.pathname + 'video';
        //alert(ws_path);
        var ws = new WebSocket(ws_path);
        //alert(ws);
        ws.onopen = function () {
            ws.send(1);
        };
        ws.onmessage = function (msg) {
            $("#video").attr('src', 'data:image/jpg;base64,' + msg.data);
            ws.send(1);
        };
        ws.onerror = function (e) {
            console.log(e);
            ws.send(1);
        };
    } else {
        // TODO video_feed is nu statish, de waarde daarvan moet eigenlijk door Flask worden gezet.
        $("#video").attr('src', "video_feed");
        log.error("WebSocket not supported");
    }
}
videoWebsocketStart();