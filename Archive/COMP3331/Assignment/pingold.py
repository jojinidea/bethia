import sys
import threading
import socket
import time

# need to give max data size - does ping send this amount?

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
        #print("Server started %s"%(self._sock), file=sys.stderr)
        pingResponse = 'PING RESPONSE'
        while True:
            try: 
                print('\nWaiting to receive message', file=sys.stderr)
                time.sleep(1)
                msg, clientAddress= self._sock.recvfrom(4096)
                clientPort = int(clientAddress[1])-50000
                print(msg.decode('utf-8') + "RECEIVED FROM" + str(clientAddress[0]) + str(clientAddress[1]))
                if self.identifyMsg(msg.decode("utf-8")) == "PEER_RESPONSE":
                    print("A peer response message was received from Peer %d"%(clientPort))
                elif self.identifyMsg(msg.decode("utf-8")) == "PEER_REQUEST":
                    # need to send response messages
                    self._sock.sendto(pingResponse.encode(), clientAddress) # sending response back to peer
                    print("A peer request message was received from Peer %d"%(clientPort))
                # need to distinguish between ping request messages and ping response messages
            except KeyboardInterrupt:
                print('Keyboard interrupt, stopping main loop', file=sys.stderr)
                sys.exit(1)

    # determines whether the message is a peer request message or a peer response message
    # if peer response, print "ping response received from..."
    # if peer request, print "ping request received from..." and send a response
    def identifyMsg(self, msg):
        if "REQUEST" in msg:
            return "PEER_REQUEST"
        elif "RESPONSE" in msg:
            return "PEER_RESPONSE"
    
    # sends messages to successors of a certain peer - this should be a thread that is invoked 
    # sends ping request message to successors - successors output on terminal 
    # send ping to address of client
    def sendPingRequest(self):
        message = 'PING REQUEST'
        #print("Hello") #- doesn't seem to be going through here
        while True:
            print("Send Ping")
            time.sleep(1)
            try:
                self._sock.sendto(message.encode(), self._immediateSuccessors[0][1])
                print("Sending pings to" + str(self._immediateSuccessors[0]), file=sys.stderr)
                self._sock.sendto(message.encode(), self._immediateSuccessors[1][1])
                print("Sending pings to" + str(self._immediateSuccessors[1]), file=sys.stderr) 
   
        
        
    #def updatePredecessor(self, address):
    #    self._immediatePredecessor = address[1]
    
    

if __name__ == "__main__":
    p1 = Peer(sys.argv[1], sys.argv[4], sys.argv[5])  
    p1.initialiseImmediateSuccessors(sys.argv[2],sys.argv[3])
    p1.bindSock()
    print(p1._immediateSuccessors)
    listen_thread = threading.Thread(target = p1.listen, args = ())
    sendPing_thread = threading.Thread(target = p1.sendPingRequest, args = ())
    sendPing_thread.start()
    listen_thread.start()
    sendPing_thread.join()
    listen_thread.join()

 
# ping successors:
# two types of messages
# ping request
    # if ping request received from any of two predecessors, output this
    # we listen to this ping request message
    # e.g. if Peer 10 receives ping request message from peer 5, it should output on its terminal: "A ping request message was received from Peer 5"
# ping response
    # if ping request message is received, the peer should send a response message to the sending peer so that the sending peer knows the receiving peer is alive
    # e.g. if peer 10 is alive, peer 5 should receive a ping response message from peer 10 and peer 5 should display:
    # it should output on the terminal "A ping response message was received from Peer 10"

