from gevent import monkey
monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=True, os=True, ssl=True, httplib=False, aggressive=True)
import simplejson
import requests

class RESTClient(object):
    """Connects to a server using a restful interface via http
    Extend this class and add functions. Look at commented example.

    """

    def __init__(self, server='localhost', port=8000, CACert=None, token=None):
        """Create a RESTClient to connect to a server.
        
        Keyword arguments:
        server -- domain to connect to (default 'localhost')
        port -- the port to connect to (default 8000)
        

        """
        self.server = server
        self.port = port
        self.restserver = None
        self.CACert = CACert
        if self.CACert:
            self.useSSL = True
            self.SSLurl = "https://%s:%i" % (self.server, self.port)
        else:
            self.useSSL = False
        self.url = "http://%s:%i" % (self.server, self.port)
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
        data -- dictionary of POST data to send with request

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
        try:
            if useSSL:
                resp = requests.post(req, data=data, verify=self.CACert).text
            else:
                resp = requests.post(req, data=data).text
        except:
            resp = ''
        return resp

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
