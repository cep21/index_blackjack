import os
import sys
try:
    import http.server
    from http.server import SimpleHTTPRequestHandler
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass = http.server.HTTPServer
except ImportError:
    import SimpleHTTPServer, SocketServer
    HandlerClass = SimpleHTTPServer.SimpleHTTPRequestHandler
    ServerClass = SocketServer.TCPServer

Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

print ("Visit http://%s:%d" % ('127.0.0.1', port))
dir_to_list = './json'
for name in os.listdir(dir_to_list):
    print ("http://%s:%d/show_chart.html?chart=%s" % ('127.0.0.1', port, os.path.splitext(name)[0]))
sa = httpd.socket.getsockname()
# print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
