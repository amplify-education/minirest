#!/usr/bin/env python
from MiniREST.RESTClient import RESTClient

class MyClient(RESTClient):
    """EXtend the RESTClient"""

    def __init__(self, server='localhost', port=8000, *args, **kwargs):
        """Accept arguments of where this client will connect to by default."""
        super(MyClient, self).__init__(server, port, *args, **kwargs)

    def hello(self, name, address=None, port=None, *args, **kwargs):
        """Accepts a name and can override default address/port"""
        return self.getResponse("hello", data = {"name": str(name), "token": self.token}, address=address, port=port, *args, **kwargs)

my_client = MyClient(token="secret")
print my_client.hello("Bob")
