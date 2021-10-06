# Speckle ML demo app (image to pointcloud)

**WARNING**: This repo is the result of a 1day hackathon and is very unstructured.

Description of directories:
 - `python-connect`: quick proof of concept way of sending pointclouds to a speckle server
 - `web-app`: The frontend Vue app
 - `server`: The final backend (includes a copy of the built frontend, for serving)

---
The `server` directory started with a clone of the ML model repository that can be found at https://github.com/ialhashim/DenseDepth

In there, there are some extra files that were added/modified:
- `cherry.py` - the startup script for this app
- `run.py` - edited from a previous script - the pre-processing and post-processing logic
- `sp.py` - utility to send pointclouds to a speckle server
- `Dockerfile` - for building a docker image with this app
- `Makefile` - build and run commands for easily build and run the docker image

To build the app:
- go into the `server` directory
- follow the instructions in the original `README.md` to download the NYU pretrained model.
- run `make build`
- edit `Makefile` to include your config
- run `make run`
