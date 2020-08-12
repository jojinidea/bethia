import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to port - associates server with server address
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# listen() puts socket into server mode and accept() waits for an incoming connection

sock.listen(1)

while True:
    # wait for a connection
    print >>sys.stderr, 'Waiting for a connection'
    connection, client_address = sock.accept() # accept() returns open connection between server and client along with address of client. Connection is actually different socket on another port. Data is read from the connection with recv() and transmitted with sendall()
    
try:
    print >>sys.stderr, 'Connection from', client_address
    
    while True:
        data = connection.recv(16)
        print >>sys.stderr, 'Received "%s"' % data
        if data:
            print >>sys.stderr, 'Sending data back to the client'
            connection.sendall(data)
        else:
            print >>sys.stderr, 'no more data from', client-address
            break

finally:
    # clean up connection
    connection.close()


I watched a talk a few months ago by Fei Fei Li on the interdisciplinary applications and "humanity" of AI, and ever since then, Ive been incredibly inspired by the opportunity to use Computer Science as a force for good and to further explore areas 

I watched a talk a few months ago by Fei Fei Li on the interdisciplinary applications of AI and ever since then, Ive been incredibly inspired by the opportunity to further explore areas that intersect Computer Science and other disciplines. 


s = socket.socket()
print "Socket successfully created"

port = 1025
s.bind(('', port)) # bind to port - have not typed any ip, instead inputted empty string, makes server listen to requests coming from other computers on network
print "socket binded to %s" %(port) 
s.listen(5)
print "socket is listening"

while True:
    c, addr = s.accept() # establish connection with client
    print "Got connection from", addr
    c.send("Thank you for connecting") # send message to client
    c.close()
