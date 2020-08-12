import sys
import threading
import socket
import time

class Peer(object):
    def __init__(self, ID, MSS, dropProb):
        self._ID = int(ID)
        self._MSS = int(MSS) 
        self._port = 50000 + int(ID)
        self._IP = 'localhost'
        self._dropProb = float(MSS)
        self._immediateSuccessors = [] 
        self._immediatePredecessor = []  
        self._shutdown = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        
    # end constructor
    
    def bindSock(self):
        self._sock.bind((self._IP, int(self._port)))
    
    def initialiseImmediateSuccessors(self, successor1, successor2):
        address1 = ('localhost', 50000 + int(successor1))
        address2 = ('localhost', 50000 + int(successor2))
        self._immediateSuccessors.append((successor1, address1))
        self._immediateSuccessors.append((successor2, address2))
      
    # listens to incoming messages 
    def listen(self):
        print("Server started %s"%(self._sock), file=sys.stderr)
        # need a thread for listening
        while True:
            print("Server")
            try: 
                print('\nWaiting to receive message', file=sys.stderr)
                data, clientAddress= self._sock.recvfrom(4096)
                print(clientAddress)
                print(data.decode('utf-8') + "RECEIVED FROMMMMMMMMMMMMMMMMMMMMMMMMMMM from" + str(clientAddress[0]) + str(clientAddress[1]))
                self._sock.sendto(data, clientAddress)
            except KeyboardInterrupt:
                print('Keyboard interrupt, stopping main loop', file=sys.stderr)
                sys.exit(1)

        
    # sends messages to successors of a certain peer - this should be a thread that is invoked 
    # send ping to address of client
    def sendPing(self):
        pings = 0
        message = 'PING {} \r'.format(pings)
        print("Hello") #- doesn't seem to be going through here
        while True:
            print("Send Ping")
            try:
                print("Sending pings to" + str(self._immediateSuccessors[0]), file=sys.stderr)
                self._sock.sendto(message.encode(), self._immediateSuccessors[0][1])
                self._sock.sendto(message.encode(), self._immediateSuccessors[1][1])
            finally: 
                pings = pings + 1     
        
        
    #def updatePredecessor(self, address):
    #    self._immediatePredecessor = address[1]
    
    

if __name__ == "__main__":
    p1 = Peer(sys.argv[1], sys.argv[4], sys.argv[5])  
    p1.initialiseImmediateSuccessors(sys.argv[2],sys.argv[3])
    p1.bindSock()
    print(p1._immediateSuccessors)
    listen_thread = threading.Thread(target = p1.listen, args = ())
    sendPing_thread = threading.Thread(target = p1.sendPing, args = ())
    sendPing_thread.start()
    listen_thread.start()
    sendPing_thread.join()
    listen_thread.join()

    
