build:
	docker build -t i2pc .

run:
	docker run -it --rm --net=host \
		-v /w/speckle/DenseDepth:/app \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-e DISPLAY=:0 \
		i2pc bash
#	docker run -it --rm -v /w/speckle/DenseDepth:/app --gpus all i2pc bash
