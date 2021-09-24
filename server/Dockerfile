FROM tensorflow/tensorflow:1.13.2-py3-jupyter

RUN pip3 install keras==2.2.4

RUN pip3 install scikit-learn scikit-image

RUN pip3 uninstall -y enum34
RUN pip3 install specklepy cherrypy
RUN pip3 install cherrypy-cors
