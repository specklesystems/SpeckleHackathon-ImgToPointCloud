FROM tensorflow/tensorflow:2.10.0-jupyter

RUN pip3 install keras==2.10.0

RUN pip3 install scikit-learn==1.1.3 scikit-image==0.19.3

RUN pip3 uninstall -y enum34
RUN pip3 install specklepy==2.9.0 cherrypy==18.8.0
RUN pip3 install cherrypy-cors==1.6

COPY . /app

WORKDIR /app

CMD ["python3", "cherry.py"]
