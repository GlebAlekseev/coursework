from flask import Flask, Response

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        # print( self.response)
        return self.response


class FlaskAppWrapper(object):
    def __init__(self, name):
        self.app = Flask(name)

    def start(self):
        self.app.run(debug=False, port=5000,threaded=True) 

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        # print("handler",handler)
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=['POST'])

