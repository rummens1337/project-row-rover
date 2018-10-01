var x, y;
var multiplier = 3.5;

function clamp(num, min, max) {
  return num <= min ? min : num >= max ? max : num;
}

function move(movedX, movedY){
	var r = movedY;
	var l = movedY;

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
	move(0, 0);

	$(".joystick").removeClass("active");
});

$( ".toggle" ).click(function() {
	$(this).toggleClass("active");
});



