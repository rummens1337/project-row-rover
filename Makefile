run:
	docker run --device /dev/gpiomem rover

run-amd64:
	docker run -v $(PWD)/settings.amd64.conf:/app/settings.conf rover

install:
	docker run --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover . --force-rm

tag = latest
push: build
	docker tag rover noeel/rover:$(tag) \
	docker push noeel/rover:$(tag)