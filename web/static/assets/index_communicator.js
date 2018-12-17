// De websocket verbinding.
var webSocket = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port);

/**
 * Als er een verbinding gemaakt wordt tussen de client en server - voor control, geen video - roept het
 * onderstaande functies aan.
 */

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

$(".toggle").click(function () {
    $(this).toggleClass("active");
});

/**
 * Zet de microfoon output aan, of uit. De functie houdt ook bij in welke staat dit zich bevindt.
 */
$(".buttonMic").click(function () {
    if($(this).hasClass("active")){
        // send enable
    }else{
        // send disable
    }
});

$(".buttonMusic").click(function () {
    if($(this).hasClass("active")){
        send("audio",0);
        document.getElementById("buttonMusic").src="/static/assets/img/play.png";
    }else{
        send("audio",1);
        document.getElementById("buttonMusic").src="/static/assets/img/pause.png";
    }
});

$(".buttonIncreaseAudio").click(function () {
    send("audio",2);
});

$(".buttonDecreaseAudio").click(function () {
    send("audio",3);
});
/**
 * Stuurt data naar het display op de rover toe, wanneer er tekst ingevoerd wordt
 */
$(".buttonDisplaySend").click(function () {
    var rovertext = document.getElementById("screenText").value;
    send("displayMsg", rovertext)
});




/**
 * Send Websocket data
 * @param request Het onderdeel wat je wilt aansturen, bijvoorbeeld "motor".
 * @param data De array aan data die je naar dit onderdeel wilt sturen, in JSON notatie.
 */

function send(request, data) {
    // TODO documentatie
    let key = "1234";
    webSocket.send(JSON.stringify(
        {
            "key": key,
            "request": request,
            // TODO data moet optioneel zijn
            "data": data
        }
    ));
//    TODO callback.
}

/**
 * VideoWebSocket
 * Start de websocket verbinding voor de video, deze is compleet gescheiden van de andere websocket verbinding.
 */

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