run:
	docker run rover

install:
	docker run --rm --privileged multiarch/qemu-user-static:register

build:
	docker build -t rover . --force-rm

build-amd64:
	docker build -t rover . --force-rm --target amd64

tag = latest
push: build
	docker manifest create noeel/rover:$(tag) --os linux --arch arm ; \
	manifest push noeel/rover:$(tag)
