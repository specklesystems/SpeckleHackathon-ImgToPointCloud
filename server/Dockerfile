FROM tensorflow/tensorflow:2.2.3-py3-jupyter

RUN pip3 install keras==2.10.0

RUN pip3 install scikit-learn scikit-image

RUN pip3 uninstall -y enum34
RUN pip3 install specklepy cherrypy
RUN pip3 install cherrypy-cors

COPY . /app

WORKDIR /app

CMD ["python3", "cherry.py"]
