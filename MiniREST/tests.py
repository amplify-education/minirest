from RESTServer import RESTServer
from RESTClient import RESTClient

def test_ping():
    server = RESTServer()
    server.start(block=False)
    client = RESTClient()
    assert client.ping() == 'PONG'
    server.stop()

def test_echo():
    server = RESTServer(default_echoes=True)
    server.start(block=False)
    client = RESTClient()
    assert client.echo('meow meow') == 'meow meow'
    server.stop()

def test_tokenEcho():
    server = RESTServer(token='secret', default_echoes=True)
    server.start(block=False)
    # Test token works
    client = RESTClient(token='secret')
    assert client.tokenEcho('meow meow') == 'meow meow'
    # Test token rejected
    badClient = RESTClient()
    assert badClient.tokenEcho('meow meow') == 'Bad Token'
    server.stop()

def test_ssl_ping():
    # Test that SSL works
    server = RESTServer(SSLKey='server.key', SSLCert='server.crt')
    server.start(block=False)
    client = RESTClient(CACert='server.crt')
    assert client.ping() == 'PONG'
    server.stop()
    # Test that bad crt rejected
    badServer = RESTServer(SSLKey='server2.key', SSLCert='server2.crt')
    badServer.start(block=False)
    assert client.ping() == ''
    badServer.stop()

def test_ssl_bad():
    server = RESTServer(SSLKey="server.key", SSLCert="server.crt", portRange=[8000,9000])
    server.start(block=False)
    client = RESTClient()
    assert client.ping() == ''
    assert client.ping() == ''
    server.stop()


