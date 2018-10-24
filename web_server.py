#!/usr/bin/env python
# Starts the web server

# TODO(whitside): Use a real web server instead of this. I can't figure out why
# the cleanup code isn't being called and this causes the server to fail to
# start sometimes because the socket is in use.

import SimpleHTTPServer
import SocketServer
import signal

PORT = 80
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

# TODO(whiteside): figure out why this isn't being called
def stop_server(signal, frame):
    print "Ctrl+C captured, stopping server"
    httpd.shutdown()
    httpd.server_close()

signal.signal(signal.SIGINT, stop_server)
signal.signal(signal.SIGTERM, stop_server)

print "serving at port", PORT
httpd.serve_forever()
