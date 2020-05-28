#!env python
# Set these to control bind host and port for tcp server
BIND_HOST, BIND_PORT = "", 11111

# Set these to control where you are connecting to
HOST, PORT = "localhost", 2121
import subprocess
from SocketServer import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM,gethostbyaddr
def datatohpinator(data):
	data=data.replace('\r','')
	url=data.split('\n')[0].split(' ')[1]
	t=["curl",url]
	for i in data.split('\n')[2::]:
		if '=' in i:
			t.append("--data")
			t.append("'"+i+"'")
		t.append("-H")
		t.append("'"+i+"'")
	print t
	try:d=subprocess.check_output(t)
	except:d='Failed'
	print d;
	return d
class SockHandler(BaseRequestHandler):
    """
    Request Handler for the proxy server.

    Instantiated once time for each connection, and must
    override the handle() method for client communication.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print "Passing data from: {}".format(self.client_address[0])
        print self.data
        received=datatohpinator(self.data)
        # Create a socket to the localhost server
        # Try to connect to the server and send data
        try:
            # Receive data from the server
            self.request.sendall(received)
        except:
			pass

if __name__ == '__main__':
    # Create server and bind to set ip
    myserver = TCPServer((BIND_HOST, BIND_PORT), SockHandler)

    # activate the server until it is interrupted with ctrl+c
    myserver.serve_forever()

