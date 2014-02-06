#!/usr/bin/env python
import random
import socket
import urlparse
import cgi
import urllib2


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


def generate_content_page(*args):
        conn = args[0]
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n')
        conn.send('<h1>Content path!</h1>')


def generate_file_page(*args):
        conn = args[0]
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n')
        conn.send('<h1>file path!</h1>')


def generate_image_page(*args):
        conn = args[0]
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n')
        conn.send('<h1>image path!</h1>')


def generate_form_page(*args):
        conn = args[0]
        conn.send("HTTP/1.0 200 OK\r\n")
        conn.send("Content-type: text/html\r\n")
        conn.send("\r\n")
        conn.send("<form action='/submit' method='GET'>")
        conn.send("First Name: <input type='text' name='firstname'></br>")
        conn.send("Last Name: <input type='text' name='lastname'></br>")
        conn.send("<button name='submitButton' type='submit'>Submit</button>")
        conn.send("</form>")


def generate_form_submission_page(*args):
        conn = args[0]
        headers = {}
        socket_data = args[1]
        fp = urllib2.StringIO(socket_data)
        parsed_url = urlparse.urlparse(socket_data)
        trimmed_url_list = parsed_url.query.split("\r\n\r\n")
        header_list = trimmed_url_list[0].split("\r\n")
        print header_list
        for entry in header_list:
            try:
                entry = entry.split(' ')
                headers[entry[0]] = entry[1]
            except:
                print 'Error parsing header dictionary. url:', parsed_url
        field_storage = cgi.FieldStorage(fp, headers)
        print socket_data
        if 'enctype:' in field_storage.headers.keys():
            if field_storage.headers['enctype:'] == 'multipart/form-data':
                print 'multiformdata!'
        else:
            try:
                #protect against empty inputs
                first_name = urlparse.parse_qs(parsed_url.query)['firstname'][0]
                last_name = urlparse.parse_qs(parsed_url.query)['lastname'][0]
                conn.send('HTTP/1.0 200 OK\r\n')
                conn.send('Content-type: text/html\r\n')
                conn.send('\r\n')
                conn.send('<h1>Hi %s %s</h1>' % (first_name, last_name))
            except:
                #if except block is hit, one or more of the fields were empty
                conn.send('HTTP/1.0 200 OK\r\n')
                conn.send('Content-type: text/html\r\n')
                conn.send('\r\n')
                conn.send('<h1>Warning, first and last name must be entered</h1>')
                #@question - why does following link not direct to the home
                #page on the first attempt, but does on the 2nd attempt?
                #conn.send('<a href=/>Home</a>')


def generate_home_page(*args):
        conn = args[0]
        conn.send('HTTP/1.0 200 OK\r\n' + 'Content-type: text/html\r\n')
        conn.send('\r\n')
        conn.send('<body>')
        conn.send('<h1>Hello, world.</h1>')
        conn.send('<p>')
        conn.send('This is Ryan Miller\'s (mill1256) Web server.</br>')
        conn.send('&nbsp&nbsp<a href=/content>Content</a></br>')
        conn.send('&nbsp&nbsp<a href=/file>File</a></br>')
        conn.send('&nbsp&nbsp<a href=/image>Image</a></br>')
        conn.send('&nbsp&nbsp<a href=/form>Form</a></br>')
        conn.send('</p>''</body>')


def generate_post_page(*args):
        conn = args[0]
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n')
        conn.send('<h1>Hello, world!</h1>')


def generate_post_form_page(*args):
        socket_data = args[1]
        parsed_url = urlparse.urlparse(socket_data)
        conn = args[0]
        try:
            #protect against empty inputs
            first_name = urlparse.parse_qs(parsed_url.query)['firstname'][0]
            last_name = urlparse.parse_qs(parsed_url.query)['lastname'][0]
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n')
            conn.send('\r\n')
            conn.send('<h1>Hi %s %s</h1>' % (first_name, last_name))
        except:
            #if except block is hit, one or more of the fields were empty
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n')
            conn.send('\r\n')
            conn.send('<h1>Warning, first and last name must be entered</h1>')


def handle_connection(conn):
    sentinel_value = '\r\n\r\n'
    current_string = ''
    socket_data = ''
    while sentinel_value != current_string:
        current_char = conn.recv(1)
        if current_char == '\r' or current_char == '\n':
            socket_data += current_char
            current_string += current_char
        else:
            socket_data += current_char
            current_string = ''

    if 'POST /form' in socket_data:
        generate_post_form_page(conn, socket_data)
    elif 'POST /' in socket_data:
        generate_post_page(conn)
    elif "GET /content" in socket_data:
        generate_content_page(conn)
    elif "GET /file" in socket_data:
        generate_file_page(conn)
    elif "GET /image" in socket_data:
        generate_image_page(conn)
    elif 'GET /form' in socket_data:
        generate_form_page(conn)
    elif '/submit?' in socket_data:
        generate_form_submission_page(conn, socket_data)
    else:
        generate_home_page(conn, socket_data)
    conn.close()


if __name__ == '__main__':
    main()



