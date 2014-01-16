#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()
host = socket.getfqdn()
port = random.randint(8000, 9999)
s.bind((host, port))

helloWorld = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n<html><body><h1>Hello World</h1>This is msu-web-dev's Web Server.</body></html>"
# @comment Don't forget to format to a max width of 80 chars for readability
print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)
print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send(helloWorld)
    c.close()
