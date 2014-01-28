#!/usr/bin/env python
import random
import socket
import time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        handle_connection(c)
        print 'Got connection from', client_host, client_port

def handle_connection(conn):
    socketData = conn.recv(1000)

    if('POST' in socketData):
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Hello, world!</h1>')
    elif ("GET /content" in socketData):
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Content path!</h1>')
    elif ("GET /file" in socketData):
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>file path!</h1>')
    elif ("GET /image" in socketData):
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>image path!</h1>')
    else:
        conn.send('HTTP/1.0 200 OK\r\n' + 'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<body>'
                  '<h1>Hello, world.</h1>' + \
                  '<p>'
                  'This is Ryan Miller\'s (mill1256) Web server.</br>' + \
                  '&nbsp&nbsp<a href=/content>Content</a></br>' + \
                  '&nbsp&nbsp<a href=/file>File</a></br>' + \
                  '&nbsp&nbsp<a href=/image>Image</a></br>' + \
                  '</p>'
                  '</body>')

    conn.close()

if __name__ == '__main__':
    main()

