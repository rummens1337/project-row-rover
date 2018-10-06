var x, y, l = 0.0, r = 0.0;
var multiplier = 3.5;

window.requestAnimationFrame = window.requestAnimationFrame
	|| window.webkitRequestAnimationFrame
	|| window.mozRequestAnimationFrame
	|| function(callback) { window.setTimeout(callback, 1000 / 60);};

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
    }
};
// What controller to lisen to
var controllerIndex = 0;
var topSpeed = 255;
// our input objects
var up = new Input.Input(inputObject.up, controllerIndex);
var down = new Input.Input(inputObject.down, controllerIndex);
var left = new Input.Input(inputObject.left, controllerIndex);
var right = new Input.Input(inputObject.right, controllerIndex);
var webSocket = new WebSocket("ws://"+window.location.hostname+":8080");

// up
up.press = function() {
	l = topSpeed * this.value;
	r = topSpeed * this.value;
	updateRL();

};
up.release = function() {
    if (down.isUp) {
    	l = 0;
    	r = 0;
        updateRL();
    }
    else down.press();
};

// down
down.press = function() {
    l = -topSpeed * this.value;
    r = -topSpeed * this.value;
    updateRL();
};
down.release = function() {
    if (down.isUp) {
        l = 0;
        r = 0;
        updateRL();
    }
    else down.press();
};

// left
left.press = function() {
    l = -topSpeed * this.value;
    r = topSpeed * this.value;
    updateRL();
};
left.release = function() {
    if (down.isUp) {
        l = 0;
        r = 0;
        updateRL();
    }
    else down.press();
};

// right
right.press = function() {
    l = topSpeed * this.value;
    r = -topSpeed * this.value;
    updateRL();
};
right.release = function() {
    if (down.isUp) {
        l = 0;
        r = 0;
        updateRL();
    }
    else down.press();
};

webSocket.onopen = function (){
    callLoop();
};

webSocket.onmessage = function (event) {
    console.log(event.data);
};


function callLoop(){

    var le = l.toFixed(0);
    var ri = r.toFixed(0);
    var msg =
        {
            'request': 'motor',
            'key': "1234",
            'data': {
                left: le,
                right: ri
            }
        };
    webSocket.send(JSON.stringify(msg));
}

function updateRL(){
    $("#l")[0].innerHTML = l.toFixed(1);
    $("#r")[0].innerHTML = r.toFixed(1);
    callLoop();
}

function clamp(num, min, max) {
  return num <= min ? min : num >= max ? max : num;
}

function move(movedX, movedY){
	r = movedY;
	l = movedY;

	if(movedX < 0){
		r -= movedX;
	}else if(movedX > 0){
		l -= movedX;
	}

	r *= multiplier;
	l *= multiplier;

	r = clamp(r, -255, 255);
	l = clamp(l, -255, 255);

	updateRL();
}

$(".joystick")[0].addEventListener('touchstart', function(e) {
	x = e.touches[0].clientX;
	y = e.touches[0].clientY;

	$(".joystick").addClass("active");
}, false);

$(".joystick")[0].addEventListener('touchmove', function(e) {
	var movedX, movedY;

	movedX = x - e.touches[0].clientX;
	movedY = y - e.touches[0].clientY;

	move(movedX, movedY);
}, false);


$(".joystick").on('touchend touchcancel', function() {
	move(0.0, 0.0);

	$(".joystick").removeClass("active");
});

$( ".toggle" ).click(function() {
	$(this).toggleClass("active");
});

$( ".buttonFlashlight" ).click(function() {
    var msg = {
        "key": "1234",
        "request": "lamp",
        "data": 0
    };

    if($(this).hasClass("active")) {
        msg.data = 1;
        webSocket.send(JSON.stringify(msg));
    } else{
        msg.data = 0;
        webSocket.send(JSON.stringify(msg));
    }
});

