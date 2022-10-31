FROM python:3.9.15-buster AS model-download

RUN pip3 install gdown

RUN gdown https://drive.google.com/uc?id=19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu

FROM tensorflow/tensorflow:2.10.0-jupyter

RUN pip3 install keras==2.10.0

RUN pip3 install scikit-learn==1.1.3 scikit-image==0.19.3

RUN pip3 uninstall -y enum34
RUN pip3 install specklepy==2.9.0 cherrypy==18.8.0
RUN pip3 install cherrypy-cors==1.6

COPY --from=model-download nyu.h5 /app/nyu.h5
COPY . /app

WORKDIR /app

CMD ["python3", "cherry.py"]
