// TODO deze javascript is echt een tering zooi, nergens documentatie en alles in een bestand gesmeten. Dit moet effe iemand opruimen.
var x, y, l = 0.0, r = 0.0;
var multiplier = 3.5;
// TODO eigenlijk moet flashlight (net als vele andere dingen hier) haar eigen class hebben.
// TODO lampstatus moet gevraagt worden van de server
// TODO alle variabelen worden met `var` aangemaakt. Het is netter om het met `let` te doen.
let flashlightStatus = 0;
let flashlightDOM = document.querySelector(".buttonFlashlight");

/**
 * Het volledige scherm wordt afgevangen, en alle inputs worden doorgegeven aan het inputObject, welke specificeerd
 * wat er moet gebeuren wanneer een bepaalde input wordt gegeven.
 * @type {{up: {key: string[], pad: string[]}, down: {key: string[], pad: string[], axes: string[]}, left: {key: string[], pad: string[]}, right: {key: string[], pad: string[], axes: string[]}, flashlight: {key: string[], pad: string[]}}}
 */

var inputObject = {
    "up": {
        "key": ["KEY_W", "UP_ARROW"],
        "pad": ["DPAD_UP", "RIGHT_TRIGGER"]
    },
    "down": {
        "key": ["KEY_S", "DOWN_ARROW"],
        "pad": ["DPAD_DOWN", "LEFT_TRIGGER"],
        "axes": ["LEFT_Y"]
    },
    "left": {
        "key": ["KEY_A", "LEFT_ARROW"],
        "pad": ["DPAD_LEFT"]
    },
    "right": {
        "key": ["KEY_D", "RIGHT_ARROW"],
        "pad": ["DPAD_RIGHT"],
        "axes": ["LEFT_X"]
    },
    "flashlight": {
        "key": ["KEY_F"],
        "pad": ["BUTTON_X"]
    }
};

// What controller to listen to
var controllerIndex = 0;
var topSpeed = 255;

// our input objects
var up = new Input.Input(inputObject.up, controllerIndex);
var down = new Input.Input(inputObject.down, controllerIndex);
var left = new Input.Input(inputObject.left, controllerIndex);
var right = new Input.Input(inputObject.right, controllerIndex);
var flashLight = new Input.Input(inputObject.flashlight, controllerIndex, flashlightDOM);

// Websocket connection
var webSocket = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port);


/**
 * Alle onderstaande functies, betreffende up/down/right/left, houden bij hoe hard de rover moet rijden
 * Deze roepen dan weer de updateRL() functie aan, welke de data verstuurd naar de rover zelf.
 */
// up
up.press = function () {
    l = topSpeed * this.value;
    r = topSpeed * this.value;

};
up.release = function () {
    if (down.isUp) {
        l = 0;
        r = 0;
    } else down.press();
};
// down
down.press = function () {
    l = -topSpeed * this.value;
    r = -topSpeed * this.value;
};
down.release = function () {
    if (down.isUp) {
        l = 0;
        r = 0;
    } else down.press();
};
// left
left.press = function () {
    l = -topSpeed * this.value;
    r = topSpeed * this.value;
};
left.release = function () {
    if (down.isUp) {
        l = 0;
        r = 0;
    } else down.press();
};
// right
right.press = function () {
    l = topSpeed * this.value;
    r = -topSpeed * this.value;
};
right.release = function () {
    if (down.isUp) {
        l = 0;
        r = 0;
    } else down.press();
};

flashLight.press = function () {
//    deze is nodig omdat anders dingen gaan crashen.
};

/**
 * Wordt aangeroepen wanneer de flashlight wordt gepressed in de UI, en houdt bij of deze aan of uit staat.
 */
flashLight.release = function () {
    if (flashlightStatus) {
        flashlightStatus = 0;
        flashlightDOM.classList.add("active");
    } else {
        flashlightStatus = 1;
        flashlightDOM.classList.remove("active");
    }
    send("lamp", flashlightStatus);
};


/**
 * Als er een verbinding gemaakt wordt tussen de client en server - voor control, geen video - roept het
 * onderstaande functies aan.
 */

webSocket.onopen = function () {
    getCompassData();
    console.log("Called onopen Function!!!");
};

webSocket.onclose = function () {
//    TODO proberen opnieuw verbinding te maken.
};

webSocket.onerror = function () {
//    TODO error handeling.
};

/**
 * Vraagt om de seconde compass data aan, mits de webSocket (variabele) verbinding open is.
 */
function getCompassData() {
    //TODO: Goede conditie maken zodat deze alleen utigevoerd wordt bij een open connectie.
    if (webSocket.OPEN) {
        setTimeout(getCompassData, 1000);
        send("compass", {
            dir: "request"
        });
    }
}

/**
 * Handelt alle inkomende berichten op de webSocket verbinding (LET OP: Geen "W" maar w, de variabele dus).
 * @param event WebSocket event welke meegegeven wordt door de WebSocket eventhandler telkens als er een bericht binnenkomt.
 */

webSocket.onmessage = function (event) {
    // TODO deze event handler is best wel vies, moet gewoon met een callback kunnen.
    // TODO want nu controleerd hij ook al het andre verkeer.
    let data = JSON.parse(event.data);
    if (data == null) {
        return;
    }
    if (data.battery !== undefined) {
        updateBatteryStatus(data.battery);
    }
    //    TODO deze elseif is te ingewikkeld, kan 1000x simpeler.
    if (data.compass !== undefined) {
        if (data.compass.dir !== undefined) {
            setCompass(parseInt(data.compass.dir));
            document.getElementById("time").innerHTML = new Date().toLocaleTimeString();
        } else {
            log.error("Compass defined, but no direction found");
        }
    }
};

/**
 * Set de waarde van het compass in de client
 * @param dir De direction waarde voor het compass display.
 */
function setCompass(dir) {
    var compassDisc = document.getElementById("compassArrowImg");
    compassDisc.style.webkitTransform = "rotate(" + dir + "deg)";
    compassDisc.style.MozTransform = "rotate(" + dir + "deg)";
    compassDisc.style.transform = "rotate(" + dir + "deg)";
}

/**
 * Kijkt of
 * @param num Het nummer dat je wilt checken
 * @param min Het minimum
 * @param max Het maximum
 * @returns min or max -
 */
function clamp(num, min, max) {
    return num <= min ? min : num >= max ? max : num;
}

/**
 *
 * @param movedX
 * @param movedY
 */

function move(movedX, movedY) {
    // TODO documenatie
    r = movedY;
    l = movedY;

    if (movedX < 0) {
        r -= movedX;
    } else if (movedX > 0) {
        l -= movedX;
    }

    r *= multiplier;
    l *= multiplier;

    r = clamp(r, -255, 255);
    l = clamp(l, -255, 255);
}

// TODO ondersteuning voor muis, of het moet weg op desktop.
$(".joystick")[0].addEventListener('touchstart', function (e) {
    x = e.touches[0].clientX;
    y = e.touches[0].clientY;

    $(".joystick").addClass("active");
}, false);

$(".joystick")[0].addEventListener('touchmove', function (e) {
    var movedX, movedY;

    movedX = x - e.touches[0].clientX;
    movedY = y - e.touches[0].clientY;

    move(movedX, movedY);
}, false);


$(".joystick").on('touchend touchcancel', function () {
    move(0.0, 0.0);

    $(".joystick").removeClass("active");
});

$(".toggle").click(function () {
    $(this).toggleClass("active");
});

$(".buttonTagLocation").click(function () {
    send("tagclicked", 1);
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
    // TODO documentatie
    // TODO port moet dynamish zijn.
    // Controlleert of de browser WebSockets ondersteund door het Window object te lezen.
    if ("WebSocket" in window) {
        var ws_path = 'ws://' + window.location.host + ":8080";
        var ws = new WebSocket(ws_path);
        ws.onopen = function () {
            // TODO testen of het nodig is om steeds een bericht terug te sturen.
            ws.send(1);
        };
        ws.onmessage = function (msg) {
            $("#video").attr('src', 'data:image/jpg;base64,' + msg.data);
            ws.send(1);
        };
        ws.onerror = function (e) {
            ws.send(1);
        };
    } else {
        alert("WebSocket not supported, please update your browser!");
    }
}


/**
 * Send battery request to rover.
 * uses `webSocket.onmessage = function (event)` to capture return
 */
function getBatteryStatus() {
    send("battery", "");
}

/**
 * update the UI with the new battery percentage.
 * @param percent int 0-100
 */
function updateBatteryStatus(percent) {
    document.querySelector(".battery").innerHTML = percent + "%";
}

/**
 * Entrypoint of the document, although not fully respected.
 */
function start() {
    setInterval(getBatteryStatus, 5000);
    videoWebsocketStart();
}
start();