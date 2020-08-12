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
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # don't know if needed
    # end constructor
    
    def bindSock(self):
        self._sock.bind((self._IP, int(self._port)))
    
    def initialiseImmediateSuccessors(self, successor1, successor2):
        address1 = ('localhost', 50000 + int(successor1))
        address2 = ('localhost', 50000 + int(successor2))
        self._immediateSuccessors.append((successor1, address1))
        self._immediateSuccessors.append((successor2, address2))
      
    # listens to incoming messages, also sends the ping response
    def listen(self):
        while True:
            try: 
                #print('\nWaiting to receive message', file=sys.stderr)
                msg, clientAddress= self._sock.recvfrom(4096)
                clientPort = int(clientAddress[1])-50000
                #print(msg.decode('utf-8') + "RECEIVED FROM" + str(clientAddress[0]) + str(clientAddress[1]))
                if self.identifyMsg(msg.decode("utf-8")) == "PEER_RESPONSE":
                    print("A peer response message was received from Peer %d"%(clientPort), file = sys.stderr)
                elif self.identifyMsg(msg.decode("utf-8")) == "PEER_REQUEST":
                    self.sendPingResponse(clientAddress) # sending response back to peer
                    print("A peer request message was received from Peer %d"%(clientPort), file=sys.stderr)
            except KeyboardInterrupt:
                print('Keyboard interrupt, stopping main loop', file=sys.stderr)
                sys.exit(1)

    # determines whether the message is a peer request message or a peer response message

    def identifyMsg(self, msg):
        if "REQUEST" in msg:
            return "PEER_REQUEST"
        elif "RESPONSE" in msg:
            return "PEER_RESPONSE"
    
    # sends ping response message to the peer who sent a ping request
    # invoked by the listen function, if the peer is sent a ping request message to the port number it is listening to
    def sendPingResponse(self, clientAddress):
        pingResponse = 'PING RESPONSE'
        self._sock.sendto(pingResponse.encode(), clientAddress) # sending response back to peer
        
    
    # sends ping request messages to the two immediate successors of a peer to check if they are alive
    def sendPingRequest(self):
        message = 'PING REQUEST'
        while True:
            #print("Send Ping")
            time.sleep(5)
            try:
                self._sock.sendto(message.encode(), self._immediateSuccessors[0][1])
                #print("Sending pings to" + str(self._immediateSuccessors[0]), file=sys.stderr)
                self._sock.sendto(message.encode(), self._immediateSuccessors[1][1])
                #print("Sending pings to" + str(self._immediateSuccessors[1]), file=sys.stderr) 
            except KeyboardInterrupt:
                print("Keyboard interrupt, stopping main loop", file = sys.stderr)
                sys.exit(1)
   
        
        
    #def updatePredecessor(self, address):
        #self._immediatePredecessor = address[1]
    
    

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

 


