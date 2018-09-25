run:
	docker run --device /dev/gpiomem -p 80:80 rover

run-amd64:
	docker run -v $(PWD)/config.amd64.ini:/app/config.ini -p 8080:80 rover

install:
	docker run --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover . --force-rm

tag = latest
push: build
	docker tag rover noeel/rover:$(tag) \
	docker push noeel/rover:$(tag)