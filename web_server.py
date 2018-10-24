#!/usr/bin/env python
# Starts the web server

import SimpleHTTPServer
import SocketServer
import signal

PORT = 80

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

def stop_server(signal, frame):
    print "Ctrl+C captured, stopping server"
    httpd.shutdown()
    httpd.server_close()

# hook SIGINT for cleanup when the script is aborted
signal.signal(signal.SIGINT, stop_server)

print "serving at port", PORT
httpd.serve_forever()
