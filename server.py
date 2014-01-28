#!/usr/bin/env python
import random
import socket
import time

def main():
  s = socket.socket()         # Create a socket object
  host = socket.getfqdn() # Get local machine name
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
  directToMain = True 
  
  if("GET /content" in socketData) :
    conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Content path!</h1>')
    directToMain = False
  if("GET /file" in socketData) :
    conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>file path!</h1>')
    directToMain = False
  if("GET /image" in socketData) :
    conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>image path!</h1>')
    directToMain = False
  if(directToMain):
    conn.send('HTTP/1.0 200 OK\r\n' + 'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is ctb\'s Web server.')

   
  conn.close()

if __name__ == '__main__':
    main()
