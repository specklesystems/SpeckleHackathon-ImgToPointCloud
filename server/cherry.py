#!/usr/bin/env python3

import cherrypy
import cherrypy_cors
import shutil
import os
from run import createPC, load_model_the_real_one

import threading

LOCK = threading.Lock()
PATH = os.path.abspath(os.path.dirname(__file__))


class App:

    @cherrypy.expose()
    def init(self):
        with LOCK:
            load_model_the_real_one()

    @cherrypy.config(**{'response.timeout': 3600})
    @cherrypy.expose()
    def upload(self, imgfile=None):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
            return 'OK'
        upload_file = '/tmp/imgfile'
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = imgfile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)

        with LOCK:
            return createPC(['/tmp/imgfile'])


cherrypy_cors.install()
config = {
    'global' : {
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Access-Control-Allow-Origin', '*')],

        'server.socket_host' : '0.0.0.0',
        'server.socket_port' : 8080,
        'server.thread_pool' : 0,
        'server.max_request_body_size' : 0,
        'server.socket_timeout' : 60
    },
    '/': {
        'cors.expose.on': True,
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, 'web'),
        'tools.staticdir.index': 'index.html',
    }
}



if __name__ == '__main__':
        cherrypy.quickstart(App(), '/', config)
