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

function callLoop(delta){
	var le = l.toFixed(0);
	var ri = r.toFixed(0);
	if(le == 0){
		le = 1;
	}
	if(ri == 0){
		ri = 1;
	}
	$.ajax({
	    url: '/api/motor',
	    method: 'PUT',
	    data: {
			key: 1234,
	    	left: le,
	    	right: ri
	    }
	});
	window.setTimeout(callLoop, 500);
}

function updateRL(){
    $("#l")[0].innerHTML = l.toFixed(1);
    $("#r")[0].innerHTML = r.toFixed(1);
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

callLoop();

