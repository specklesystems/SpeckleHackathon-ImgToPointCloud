build:
	docker build -t i2pc .

run:
	docker run -it --rm --net=host \
		-v /w/speckle/SpeckleHackathon-ImgToPointCloud/server:/app \
		i2pc bash
#	docker run -it --rm -v /w/speckle/DenseDepth:/app --gpus all i2pc bash
