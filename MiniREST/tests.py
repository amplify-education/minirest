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


