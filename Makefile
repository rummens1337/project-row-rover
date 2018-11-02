p=8080
tag = latest
target=main.py

run:
	docker run --privileged -it --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 rover

run-amd64:
	docker run -it -v /${CURDIR}/settings.amd64.conf:/app/settings.conf -p $(p):80 rover

run-current:
	docker run -it -v $(PWD)/:/app/ -v $(PWD)/$(target):/app/main.py --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 rover

run-current-amd64:
	docker run -it -v /${CURDIR}/:/app/ -v /${CURDIR}/settings.amd64.conf:/app/settings.conf -v /${CURDIR}/$(target):/app/main.py -p $(p):80 rover

install:
	docker run -it --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover .

push: build
	docker tag rover noeel/rover:$(tag)
	docker push noeel/rover:$(tag)

# TODO build documentation

# TODO run tests
