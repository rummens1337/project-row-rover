p= 80
vp= 8080
tag = latest
target= supervisord

run:
	docker run -it --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 rover

run-amd64:
	docker run -it -v $(PWD)/settings.amd64.conf:/app/settings.conf -p $(p):80 -p $(vp):8080 rover

run-current:
	docker run -it -v $(PWD)/:/app/ --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

run-current-amd64:
	docker run -it -v $(PWD)/:/app/ -v $(PWD)/settings.amd64.conf:/app/settings.conf -p $(p):80 -p $(vp):8080 --entrypoint $(target) rover

install:
	docker run -it --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover .

push: build
	docker tag rover noeel/rover:$(tag)
	docker push noeel/rover:$(tag)

# TODO build documentation

# TODO run tests
