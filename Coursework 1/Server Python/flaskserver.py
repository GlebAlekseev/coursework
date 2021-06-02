from flask import Flask, Response

class FlaskAppWrapper(object):
    def __init__(self, name):
        self.app = Flask(name)

    def start(self):
        self.app.run(debug=False, port=5000,threaded=True) 

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=['POST'])

