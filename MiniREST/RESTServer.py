# vim: ts=4 et filetype=python
# Server
from gevent.pywsgi import WSGIServer, WSGIHandler
# Post Parsing
from urlparse import parse_qs
# Response packaging
import simplejson
import random
import warnings
from ssl import SSLError

responseTypes = { 'plaintext': [('content-type','text/plain')] }
responseCodes = { 200: '200 OK', 400: '400 Bad Request', 403: '403 Forbidden', 404: '404 NOT FOUND'}

#A hack to ignore SSL errors in a somewhat sane way
class WS(WSGIServer):
    """ A wrapper on WSGIServer. Allows handling of ssl errors """

    def wrap_socket_and_handle(self, client_socket, address):
        try:
            WSGIServer.wrap_socket_and_handle(self, client_socket, address)
        except SSLError as e:
            warnings.warn("Got ssl error ({0}) from {1}:{2}".format(e, address[0], address[1]))

class RESTServer(object):
    """RESTServer - creates a new RESTServer instance.
    Extend this class and register new functions with 'registerFunction'

    """

    max_connection_attempts = 100

    def __init__(self,bind='0.0.0.0',port=8000, portRange=None, SSLKey=None, SSLCert=None, token=None, default_echoes=False):
        """Create a RESTServer. Call 'start' to start the server.

        Keyword arguments:
        bind -- the address to which the server binds (default '0.0.0.0')
        port -- the port on which the server listens (default 8000)
        portRange -- choose first available port to listen on from two length array

        """
        # Bot for possible callbacks
        self.bot = None
        # Registered response functions
        self.responses = {
                'ping': self._pong,
        }
        self.useToken = {
                'ping': False
        }
        if default_echoes:
            self.registerFunction('', self._main, token=False)
            self.registerFunction('echo', self._echo, token=False)
            self.registerFunction('tokenEcho', self._tokenEcho, token=True)

        self.portRange = portRange

        self.bind = bind
        self.port = port
        self.SSLKey = SSLKey
        self.SSLCert = SSLCert
        self.server = None
        if token == None:
            self.token = ""
        else:
            self.token = token

    def start(self,block=True):
        """Starts the server and binds to the port.

        Keyword arguments:
        block -- boolean wether to run sync(True) or async(False) (default 'True')

        """
        if self.server != None:
            return True
        if self.portRange is None:
            self.portRange = [self.port, self.port+1]
        else:
            self.port = self.portRange[0]
        count = 0
        error = None
        while count < self.max_connection_attempts:
            try:
                if self.SSLKey and self.SSLCert:
                    self.server = WS((self.bind, self.port), self._respond, keyfile=self.SSLKey, certfile=self.SSLCert)
                else:
                    self.server = WSGIServer((self.bind, self.port), self._respond)
                if not block:
                    self.server.start()
                    return True
                else:
                    self.server.serve_forever()
                break
            except Exception:
                if count >= self.max_connection_attempts-1:
                    raise
                self.port = random.randrange(self.portRange[0], self.portRange[1])
            count += 1
        if count >= self.max_connection_attempts:
            return False
        else:
            return True

    def started(self):
        """Returns True/False for wether server is started

        """
        return self.server.started

    def stop(self):
        """Stop the server.

        """
        self.server.stop()

    def _parsePOST(self, env):
        """Parses the POST data and returns a dictionary.
        Returns empty on error.

        Keyword argument:
        env -- the request variables to parse of POST data

        """
        try:
            data = env['wsgi.input']
            return simplejson.loads(parse_qs(data.read())['data'][0])
        except KeyError:
            return { }

    def _respondMalformed(self, start_response):
        """Create an http 400 error response, complaining about malformed request.

        Keyword Arguments:
        start_response -- the response request

        """
        start_response(responseCodes[400], responseTypes['plaintext'])
        return 'MALFORMED'

    def registerFunction(self, name, f, token=None):
        """Adds a function to the response table.
        Must have (self, env, start_response) as parameters.

        Keyword arguments:
        name -- the string name. Function available at: http://localhost:port/name
        f -- the reponse function
        token -- True/False wether to authenticate Token for function

        """
        if token == None:
            token = False
        self.useToken[name] = token
        self.responses[name] = f

    def registerBot(self, bot):
        """Register a bot for possible interaction.
        Available at self.bot

        Keyword arguments:
        bot -- the bot to register

        """
        self.bot = bot

    def _respond(self, env, start_response):
        """Parses all http requests and forwards them using the function table.
        Only one level of mapping available. Returns '404' if no function.
        eo
        "" "/" "//" etc map to '' function
        "/abc" and "/abc/" map to "abc" function

        Keyword arguments:
        env -- variables describing request
        start_response -- used for creating the response

        """
        # Split request
        path = str.split(env['PATH_INFO'],'/')
        # Path is either ("" || "/") => '' or ("/abc/...") => "abc"
        if len(path)<1:
            path = ''
        else:
            path = path[1]

        post = self._parsePOST(env)
        # Call appropriate function or return 404
        try :
            if self.useToken[path] and self.token != post['token']:
                start_response(responseCodes[403], responseTypes['plaintext'])
                return 'Bad Token'
            f = self.responses[path]
        except KeyError:
            start_response(responseCodes[404], responseTypes['plaintext'])
            return ('Not Found',)

        try:
            return f(env, start_response, post)
        except KeyError:
            return self._respondMalformed(start_response)


    def _checkToken(self, token):
        if token != self.token:
            raise KeyError

    # pong - reply to a ping
    def _pong(self, env, start_response, post):
        """Responds with a 'PONG'

        """
        start_response(responseCodes[200], responseTypes['plaintext'])
        return "PONG"

    # main - replies hello
    def _main(self, env, start_response, post):
        """Reponds to top level request with a 'HELLO'

        """
        start_response(responseCodes[200], responseTypes['plaintext'])
        return "HELLO"

    # echo - replies with sent 'message'
    def _echo(self, env, start_response, post):
        """Responds with what is sent in POST['message']

        """
        message = post['message']
        start_response(responseCodes[200], responseTypes['plaintext'])
        return message

    # tokenEcho - only echo back if user provides appropritate token
    def _tokenEcho(self, env, start_response, post):
        self._checkToken(post['token'])
        message = post['message']
        start_response(responseCodes[200], responseTypes['plaintext'])
        return message


#if __name__ == '__main__':
    #s = RESTServer(SSLKey='server.key', SSLCert='server_127.crt', default_echoes=True)
    #s = RESTServer(default_echoes=True)
    #s.start()
