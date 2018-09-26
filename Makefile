run:
	docker run --device /dev/i2c-1 --device /dev/vchiq -p 80:80 rover

run-amd64:
	docker run -v $(PWD)/settings.amd64.conf:/app/settings.conf -p 8080:80 rover

target=main.py
run-current:
	docker run -v $(PWD)/:/app/ -v $(PWD)/$(target):/app/main.py --device /dev/i2c-1 --device /dev/vchiq -p 80:80 rover

run-current-amd64:
	docker run -v $(PWD)/:/app/ -v $(PWD)/settings.amd64.conf:/app/settings.conf -v $(PWD)/$(target):/app/main.py -p 8080:80 rover

install:
	docker run --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover . --force-rm

tag = latest
push: build
	docker tag rover noeel/rover:$(tag) \
	docker push noeel/rover:$(tag)
