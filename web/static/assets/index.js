var x, y, l = 0.0, r = 0.0;
var multiplier = 3.5;

window.requestAnimationFrame = window.requestAnimationFrame
	|| window.webkitRequestAnimationFrame
	|| window.mozRequestAnimationFrame
	|| function(callback) { window.setTimeout(callback, 1000 / 60);};

function callLoop(delta){
	var le = l.toFixed(0);
	var ri = r.toFixed(0);
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

	$("#l")[0].innerHTML = l.toFixed(1);
	$("#r")[0].innerHTML = r.toFixed(1);
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

