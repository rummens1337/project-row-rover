p= 80
vp= 8080
tag = latest
target= "python3 init.py"


# TODO privileged mode moet eigenlijk niet, kunnen beter cap-add ofzo gebruiken

# TODO je moet een log kunnen "tailen" wanneer je een run command doet.
run:
	docker run --privileged -it ${CURDIR}/appdata:/appdata --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-amd64:
	docker run -it -v ${CURDIR}/settings.amd64.conf:/app/settings.conf -v ${CURDIR}/appdata:/appdata -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-current:
	docker run --privileged -it -v ${CURDIR}/:/app/ --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-current-amd64:
	docker run -it -v ${CURDIR}/settings.amd64.conf:/app/settings.conf -v ${CURDIR}/appdata:/appdata -v ${CURDIR}/:/app/ -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

install:
	docker run -it --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover .

push: build
	docker tag rover noeel/rover:$(tag)
	docker push noeel/rover:$(tag)

# TODO bestanden moeten niet als sudo worden aangemaakt.
clear-logs:
	sudo rm log/*.log*

# TODO build documentation

# TODO run tests
