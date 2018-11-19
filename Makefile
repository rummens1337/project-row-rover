p= 80
vp= 8080
tag = latest
target= supervisord

# TODO privileged mode moet eigenlijk niet, kunnen beter cap-add ofzo gebruiken
run:
	docker run --privileged -it --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-amd64:
	docker run -it -v ${CURDIR}/settings.amd64.conf:/app/settings.conf -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-current:
	docker run --privileged -it -v $(PWD)/:/app/ --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-current-amd64:
	docker run -it -v ${CURDIR}/:/app/ -v ${CURDIR}/settings.amd64.conf:/app/settings.conf -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover


install:
	docker run -it --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover .

push: build
	docker tag rover noeel/rover:$(tag)
	docker push noeel/rover:$(tag)

# TODO build documentation

# TODO run tests
