#!/usr/bin/env python
from MiniREST.RESTServer import RESTServer, responseCodes, responseTypes

class MyServer(RESTServer):
    """Extend the RESTServer"""

    def __init__(self, *args, **kwargs):
        """Accept arguments. Ie bind address/port"""
        """Call superclass constructor"""
        super(MyServer, self).__init__(*args, **kwargs)
        """Register a callback function.
        This one will respond to http://ip/hello.
        Only one level of calling. http://ip/hello/meow will route to same callback"""
        self.registerFunction('hello', self.hello, token=True)

    def hello(self, env, start_response, post):
        """Callback function"""
        """env contains raw data"""
        """Superclass processes recieved data sent via RESTClient into 'post' param'"""
        name = post['name']
        """Start a response, HTTP 200, type plaintext"""
        start_response(responseCodes[200], responseTypes['plaintext'])
        """Content of our message"""
        return "Hello %s" % name

"""Create an instance of your server."""
my_server = MyServer(token="secret")
"""
You can also pass in a port range and it will start on the first available port
SSL and tokens are optional.
my_server = MyServer(bind='0.0.0.0', port=8000, SSLKey="ssl.key", SSLCert="ssl.crt", token="secret_auth_token")
my_server = MyServer(bind='0.0.0.0', portRange=[8000,10000], SSLKey="ssl.key", SSLCert="ssl.crt", token="secret_auth_token")
"""
"""Start in blocking / non-blocking mode"""
my_server.start(block=True)
