#!env python
#Author : Tarik Bakir https://github.com/TRKBKR

# Set these to control bind host and port for tcp server
BIND_HOST, BIND_PORT = "", 60535

# Set these to control where you are connecting to
HOST, PORT = "localhost", 2121

from SocketServer import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM,gethostbyaddr
def datatohpinator(data):
        if 'http' not in data.split('\n')[0]:
            print '===> No HTTP'
            x=data.split('\n')[0].split(' ')[1].split(':')
            H=x[0]
            try:HOST=gethostbyaddr(H)[-1][0]
            except:
                if H.find('.') == 3:
                    HOST=H.split(':')[0]
                else:HOST=H
            return HOST,int(x[1])
	x=data.split('\n')[0].split(' ')[1].split('/')
	print '====> ',x
        P=x[0]
        H=x[2]
        if ':' in H:
            PORT=int(H.split(':')[-1])
        elif P.lower()=='https:':
            PORT=443
	else:
	    PORT=80
	try:HOST=gethostbyaddr(H)[-1][0]
	except:
            if H.find('.') == 3:
                HOST=H.split(':')[0]
            else:HOST=H
        return HOST,PORT
	
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
        HOST,PORT=datatohpinator(self.data)
        print HOST,PORT
        # Create a socket to the localhost server
        sock = socket(AF_INET, SOCK_STREAM)
        # Try to connect to the server and send data
        try:
            sock.connect((HOST, PORT))
            sock.sendall(self.data)
            # Receive data from the server
            while 1:
                received = sock.recv(1024)
                if not received: break
                # Send back received data
                self.request.sendall(received)
        finally:
            sock.close()

if __name__ == '__main__':
    # Create server and bind to set ip
    myserver = TCPServer((BIND_HOST, BIND_PORT), SockHandler)

    # activate the server until it is interrupted with ctrl+c
    myserver.serve_forever()

