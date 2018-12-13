p= 80
vp= 8080
tag = latest


# TODO je moet een log kunnen "tailen" wanneer je een run command doet.

run:
# TODO privileged mode moet eigenlijk niet, kunnen beter cap-add ofzo gebruiken
	docker run --privileged -it -v ${CURDIR}/appdata:/appdata --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 rover

run-amd64:
	docker run -it -v ${CURDIR}/settings.amd64.template.conf:/app/settings.conf -v ${CURDIR}/appdata:/appdata -p $(p):80 -p $(vp):8080 rover && tail -f appdata/log/rover.log

run-current:
	docker run --privileged -it -v ${CURDIR}/:/app/ -v ${CURDIR}/appdata:/appdata --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 rover

run-current-amd64:
	docker run -it -v ${CURDIR}/settings.amd64.template.conf:/app/settings.conf -v ${CURDIR}/appdata:/appdata -v ${CURDIR}/:/app/ -p $(p):80 -p $(vp):8080 rover

bash:
# TODO target/entrypoint maken ipv `run-bash`
	docker run -it -v ${CURDIR}/appdata:/appdata -p $(p):80 -p $(vp):8080 --entrypoint bash rover
	
bash-current:
	docker run -it -v ${CURDIR}/appdata:/appdata --device /dev/gpiomem -v ${CURDIR}/:/app/ -p $(p):80 -p $(vp):8080 --entrypoint bash rover

install:
	docker run -it --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover .

push: build
	docker tag rover noeel/rover:$(tag)
	docker push noeel/rover:$(tag)

# TODO bestanden moeten niet als sudo worden aangemaakt.
clear-appdata:
	sudo rm appdata -rf

# TODO build documentation

# TODO run tests
