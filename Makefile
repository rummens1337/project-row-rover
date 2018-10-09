p=8080
tag = latest
target=main.py

run:
	docker run --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 rover

run-amd64:
	docker run -v $(PWD)/settings.amd64.conf:/app/settings.conf -p $(p):80 rover

run-current:
	docker run -v $(PWD)/:/app/ -v $(PWD)/$(target):/app/main.py --device /dev/i2c-1 --device /dev/gpiomem --device /dev/vchiq -p $(p):80 rover

run-current-amd64:
	docker run -v $(PWD)/:/app/ -v $(PWD)/settings.amd64.conf:/app/settings.conf -v $(PWD)/$(target):/app/main.py -p $(p):80 rover

install:
	docker run --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover .

push: build
	docker tag rover noeel/rover:$(tag)
	docker push noeel/rover:$(tag)

test:
	docker run -v $(PWD)/settings.amd64.conf:/app/settings.conf -p $(p):80 rover
# TODO build documentation
