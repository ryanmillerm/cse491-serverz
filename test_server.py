import server


class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """

    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r

        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.


def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n' + 'Content-type: text/html\r\n'
                       '\r\n'
                       '<body>'
                       '<h1>Hello, world.</h1>'
                       '<p>'
                       'This is Ryan Miller\'s (mill1256) Web server.</br>'
                       '&nbsp&nbsp<a href=/content>Content</a></br>'
                       '&nbsp&nbsp<a href=/file>File</a></br>'
                       '&nbsp&nbsp<a href=/image>Image</a></br>'
                       '&nbsp&nbsp<a href=/form>Form</a></br>'
                       '</p>'
                       '</body>')
     
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_content_connection():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n'
                       'Content-type: text/html\r\n'
                       '\r\n'
                       '<h1>Content path!</h1>')

    server.handle_connection(conn)
    assert expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)


def test_handle_file_connection():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n'
                       'Content-type: text/html\r\n'
                       '\r\n'
                       '<h1>file path!</h1>')
    server.handle_connection(conn)
    assert expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)


def test_handle_image_connection():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n'
                       'Content-type: text/html\r\n'
                       '\r\n'
                       '<h1>image path!</h1>')

    server.handle_connection(conn)
    assert expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)


def test_handle_post_request():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n'
                       'Content-type: text/html\r\n'
                       '\r\n'
                       '<h1>Hello, world!</h1>')

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_form_connection():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = ("HTTP/1.0 200 OK\r\n"
                       "Content-type: text/html\r\n"
                       "\r\n"
                       "<form action='/submit' method='GET'>"
                       "First Name: <input type='text' name='firstname'></br>"
                       "Last Name: <input type='text' name='lastname'></br>"
                       "<button name='submitButton'"
                       " type='submit'>Submit</button>"
                       "</form>")

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_form_valid_submission():
    conn = FakeConnection("GET /submit?firstname=Ryan&lastname=Miller&submitButton= HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n' +
                       'Content-type: text/html\r\n' +
                       '\r\n' +
                       '<h1>Hi Ryan Miller</h1>')

    server.handle_connection(conn)
    print expected_return
    print repr(conn.sent)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_form_post():
    conn = FakeConnection("POST /form/submit? HTTP/1.0"
                          "&firstname=Ryan&lastname=Miller\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n' +
                       'Content-type: text/html\r\n' +
                       '\r\n' +
                       '<h1>Hi Ryan Miller\r\n\r\n</h1>')

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_form_post_invalid():
    conn = FakeConnection("POST /form/submit? HTTP/1.0"
                          "&firstname=&lastname=\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n' +
                       'Content-type: text/html\r\n' +
                       '\r\n' +
                       '<h1>Warning, first and last name must be entered</h1>')

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_handle_form_invalid_submission():
    conn = FakeConnection("GET /submit?firstname=&lastname=&submitButton= HTTP/1.0\r\n\r\n")
    expected_return = ('HTTP/1.0 200 OK\r\n'
                       'Content-type: text/html\r\n'
                       '\r\n'
                       '<h1>Warning, first and last name must be entered</h1>')

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

    
def test_handle_form_invalid_submission():
    conn = FakeConnection("GET /iAmAGoon HTTP/1.0\r\n\r\n")
    expected_return = ('src="http://www.finerminds.com')

    server.handle_connection(conn)
    assert expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)
