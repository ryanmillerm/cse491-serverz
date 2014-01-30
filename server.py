#!/usr/bin/env python
import random
import socket
import time
import urlparse



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
    elif('GET /form' in socketData):
        conn.send("HTTP/1.0 200 OK\r\n" + \
                  "Content-type: text/html\r\n"
                  "\r\n" + \
                  "<form action='/submit' method='GET'>" +  \
                  "First Name: <input type='text' name='firstname'></br>" + \
                  "Last Name: <input type='text' name='lastname'></br>" + \
                  "<button name='submitButton' type='submit'>Submit</button>" + \
                  "</form>")
    elif('/submit' in socketData):
         parsed_url = urlparse.urlparse(socketData)
         try:    
           #protect against empty inputs
           first_name = urlparse.parse_qs(parsed_url.query)['firstname'][0]
           last_name = urlparse.parse_qs(parsed_url.query)['lastname'][0]
           conn.send('HTTP/1.0 200 OK\r\n' + \
                     'Content-type: text/html\r\n' + \
                     '\r\n')
           conn.send('<h1>Hi %s %s</h1>' % (first_name, last_name))
         except:
            #if except block is hit, one or more of the fields were empty
            conn.send('HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n')
            conn.send('<h1>Warning, first and last name must be entered</h1>')
            #@question - why does following link not direct to the home
            #page on the first attempt, but does on the 2nd attempt? 
            #conn.send('<a href=/>Home</a>')
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
                  '&nbsp&nbsp<a href=/form>Form</a></br>' + \
                  '</p>'
                  '</body>')

    conn.close()

if __name__ == '__main__':
    main()

