FROM tensorflow/tensorflow:1.13.2-py3-jupyter

RUN pip3 install keras==2.2.4

RUN pip3 install scikit-learn==0.24.2 scikit-image==0.17.2

RUN pip3 uninstall -y enum34
RUN pip3 install specklepy==2.3.2 cherrypy==18.6.1
RUN pip3 install cherrypy-cors==1.6

COPY . /app

WORKDIR /app

CMD ["python3", "cherry.py"]
