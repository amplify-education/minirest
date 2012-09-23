RCUBIC
======

Introduction
------------

MiniREST is a small framework for sending and receiving POST messages with SSL and token authentication.

.. contents::


Getting Started
---------------

Installation
````````````

Prerequisites
:::::::::::::
 * python libraries:

   - gevent__

     + greenlet__

   - lxml__

   - simplejson__ (standard in python > 2.6)

   - python-requests__

__ http://www.gevent.org/
__ http://pypi.python.org/pypi/greenlet
__ http://lxml.de/
__ http://pypi.python.org/pypi/simplejson/
__ http://docs.python-requests.org/en/latest/index.html

How to install
::::::::::::::
#. Use *setup.py*

Usage guide
-----------

Server
``````
The sever uses pywsgi. Extend the RESTSever class, implement local methods, and register them. URLs are only routed to functions based on the first value: ie "http://ip/hello" and "http://ip/hello/meow" will both be forwarded to the same callback function.

Client
``````
The client uses python-requests. Extend the RESTClient class, and implement local methods. You can specify the address/port for each call. If they are not specified the default will be used. Arguments can be passed in as a dictionary of "string -> int/string".

Authentication
``````````````
If SSL is turned on, the Server will listen for SSL connections. A token can be used to limit access to function calls from the outside. The client will receive an SSLError if the SLL authentication fails, a ConnectionError when trying to connect to an SSL server without using SSL, and a 403 message 'Bad Token', if the token doesn't match.

Examples
````````
Please take a look at example_server.py, example_client.py, and tests.py.
