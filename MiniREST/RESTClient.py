# vim: ts=4 et filetype=python


# This file is part of MiniREST
#
#Copyright (c) 2012 Wireless Generation, Inc.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


from gevent import monkey
monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=True, os=True, ssl=True, httplib=False, aggressive=True)
import simplejson
import requests
from requests import ConnectionError
import logging

class RESTClient(object):
    """Connects to a server using a restful interface via http
    Extend this class and add functions. Look at commented example.

    """

    def __init__(self, server='localhost', port=8000, ssl=False, CACert=False, token=None):
        """Create a RESTClient to connect to a server.

        Keyword arguments:
        server -- domain to connect to (default 'localhost')
        port -- the port to connect to (default 8000)


        """
        self.server = server
        self.port = port
        self.restserver = None
        self.CACert = CACert
        self.useSSL = ssl
        if self.useSSL:
            self.SSLurl = "https://%s:%i" % (self.server, self.port)
        else:
            self.useSSL = False
        self.url = "http://%s:%i" % (self.server, self.port)
        if token == None:
            self.token = ""
        else:
            self.token = token

    def registerRESTServer(self, restserver):
        """Register a RESTSerer for event registration.

        Keyword arguments:
        restserver -- the server to register

        """
        self.restserver = restserver


    def getResponse(self, link, data=None, address=None, port=None, SSL=True):
        """Execute a get request and return the response.

        Keyword arguments:
        link -- the string to append to the base domain
        data -- dictionary of POST data to send with request or None on error

        """
        # By default try using SSL
        useSSL = SSL and self.useSSL
        if not data:
            data = { }
        data = {'data': simplejson.dumps(data)}
        # No address/port specified so use constructor default
        if not address and not port:
            if useSSL:
                req = ("%s/%s" % (self.SSLurl, link))
            else:
                req = ("%s/%s" % (self.url, link))
        # Use a specified url
        else:
            if useSSL:
                req = ("https://%s:%i/%s" % (address, port, link))
            else:
                req = ("http://%s:%i/%s" % (address, port, link))
        # Now get it
        resp = ''
        try:
            if useSSL:
                resp = requests.post(req, data=data, verify=self.CACert).text
            else:
                resp = requests.post(req, data=data).text
            return resp
        except ConnectionError:
            logging.warning("Failed to send request %s to %s." %(data, req))
            return None

    def ping(self, *args):
        """Test function which sends a ping to the server.

        """
        return self.getResponse("ping", *args)

    # example function
    # echo - asks the bot to echo back the message
    def echo(self, message, *args):
        return self.getResponse("echo", data = {"message": message}, *args)

    def tokenEcho(self, message, *args):
        return self.getResponse("tokenEcho", data = {"message": message, "token": self.token}, *args)
