FROM tensorflow/tensorflow:2.2.3-py3-jupyter

RUN pip3 install keras==2.10.0

RUN pip3 install scikit-learn==0.24.2 scikit-image==0.17.2

RUN pip3 uninstall -y enum34
RUN pip3 install specklepy==2.6.7 cherrypy==18.8.0
RUN pip3 install cherrypy-cors==1.6

COPY . /app

WORKDIR /app

CMD ["python3", "cherry.py"]
