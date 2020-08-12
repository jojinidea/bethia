import sys
import threading
import socket
import time
import re
import codecs
import select
import random

class Peer(object):
    def __init__(self, ID, MSS, dropProb):
        self._ID = int(ID)
        self._MSS = int(MSS) 
        self._port = 50000 + int(ID)
        self._IP = 'localhost'
        self._dropProb = float(dropProb)
        self._immediateSuccessors = [] 
        self._immediatePredecessors = [] 
        self._shutdown = False
        self._UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._TCPServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # end constructor
    
    def bindSock(self):
        self._UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self._UDPSock.bind((self._IP, int(self._port)))
        self._TCPServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._TCPServerSock.bind((self._IP, int(self._port)))
        
    def initialiseImmediateSuccessors(self, successor1, successor2):
        address1 = ('localhost', 50000 + int(successor1))
        address2 = ('localhost', 50000 + int(successor2))
        self._immediateSuccessors.append((successor1, address1))
        self._immediateSuccessors.append((successor2, address2))
      
    # listens to incoming messages, also sends the ping response
    def UDPlisten(self):
        while True:
            try: 
                msg, clientAddress= self._UDPSock.recvfrom(4096)
                clientPort = int(clientAddress[1])-50000
                #if self.identifyMsg(msg) == "PING_RESPONSE":
                    #print("A peer response message was received from Peer %d"%(clientPort))
                if self.identifyMsg(msg) == "PING_REQUEST":
                    self.sendPingResponse(clientAddress) # sending response back to peer
                    self.updatePredecessors(clientPort)
                    #print("A peer request message was received from Peer %d"%(clientPort))
                if self.identifyMsg(msg) == "START_FILE_TRANSFER":
                    print("We now start receiving the file")
                    self.receiveFile()
                #if self.identifyMsg(msg) == "END_FILE_TRANSFER":
                #    print("We have received the file")
                #if self.identifyMsg(msg) == "FILE_TRANSFER":
                #    print("FILE TRANSFER STARTING!!!")
                #    self.receiveFile(msg, clientAddress)
            except KeyboardInterrupt:
                print('Keyboard interrupt, stopping main loop', file=sys.stderr)
                sys.exit(1)

    # determines whether the message is a peer request message, peer response message, a file request/file response message or if the message contains the data of the file transfer
    def identifyMsg(self, msg):
    # need to incrementally decode first 12 bytes - see if PING/FILE in it, if so, decode whole message, if NOT and if ***HEADER** in it, it is file
        dec = codecs.getincrementaldecoder('utf8')()
        identifier = ""
        identifier += dec.decode(msg[0:11])
        if "PING" in identifier:
            msg = msg.decode('utf-8')
            if "PING_REQUEST" in msg:
                #print("ping request")
                return "PING_REQUEST"
            elif "PING_RESPONSE" in msg:
                #print("ping response")
                return "PING_RESPONSE"
        if "FILE" in identifier:
            msg = msg.decode('utf-8')
            if "FILE_REQUEST" in msg:
                return "FILE_REQUEST"
            elif "FILE_RESPONSE" in msg:
                return "FILE_RESPONSE"
        if "START" in identifier:
            msg = msg.decode('utf-8')
            if ("START_TRANSFER") in msg:
                return "START_FILE_TRANSFER"
        if "END" in identifier:
            msg = msg.decode('utf-8')
            if ("END_TRANSFER") in msg:
                return "END_FILE_TRANSFER"
        if "HEADER" in identifier:
            print("file transfer with header")
            return "FILE_DATA"
        if "ACK" in identifier:
            #print("Identifier is", identifier)
            #print("We have an ACK MSG")
            return "ACK"
        
    # sends ping response message to the peer who sent a ping request
    def sendPingResponse(self, clientAddress):
        pingResponse = 'PING_RESPONSE'
        self._UDPSock.sendto(pingResponse.encode(), clientAddress)        
    
    # sends ping request messages to the two immediate successors of a peer to check if they are alive
    def sendPingRequest(self):
        message = 'PING_REQUEST'
        while True:
            time.sleep(2)
            try:
                self._UDPSock.sendto(message.encode(), self._immediateSuccessors[0][1])
                self._UDPSock.sendto(message.encode(), self._immediateSuccessors[1][1])
            except KeyboardInterrupt:
                print("Keyboard interrupt, stopping main loop", file = sys.stderr)
                sys.exit(1)
    
    def updatePredecessors(self, predecessorPort):
        if predecessorPort not in self._immediatePredecessors:
            self._immediatePredecessors.append(predecessorPort)
        self._immediatePredecessors.sort()
        #print("Immediate predecessors are", self._immediatePredecessors)
        
    # applies hash function on fileID to compute location
    def hashFunction(self, fileID):
        return (fileID % 256)

    # handles file requests - continuously waits for input. If input of the form request X, we call the find File Location function
    def handleFileRequest(self):       
        while True:
            userInput = input()
            print(userInput)
            if "request" in userInput:
                fileID = int(re.findall(r'\d+',userInput)[0]) # extracts file ID from input
                print(fileID)
                fileLocation = (self.hashFunction(fileID)) # applies hash function on file ID
                requestingPeer = self._ID
                self.findFileLocation(fileID, requestingPeer, fileLocation, self._ID)
                    
    # determines location of file, we continue calling request file until we are closer to the file's location than our successor - BUG NEED TO KEEP TRACK OF SUCCESSOR AND PREDECESSOR
    def findFileLocation(self, fileID, requestingPeer, fileLocation, predecessorID):
        successorLocation = self._immediateSuccessors[0][1][1]
        successorID = successorLocation - 50000
        peerID = self._ID
        # REMOVE LOGIC FROM THIS SECTION
        if self.forwardMessage(fileLocation) == True:
            print("File %d is not stored here.\n File request message has been forwarded to my successor %d"%(fileLocation, successorID), file = sys.stderr)
            self.sendRequestFileMsg(requestingPeer, fileLocation, successorLocation, predecessorID, fileID)
        else: # we are the closest peer
            print("File %d is here.\n A response message, destined for Peer %d, has been sent.\n"%(fileLocation, requestingPeer), file = sys.stderr)
            self.sendFileResponse(requestingPeer, fileID)
            self.sendFile(requestingPeer, fileID)
            

    # returns true if current peer is closest peer and false otherwise
    def closestPeer(self, distances): 
        if distances[1] <= distances[0] and distances[1] <= distances[2]: # that means we are the closest peer
            print("Returning true")
            return True
        print("Returning false")
        return False

    def findImmediatePredecessor(self):
        peerID = self._ID
        if self._immediatePredecessors[1] <= peerID:
            return int(self._immediatePredecessors[1])
        else:
            return int(self._immediatePredecessors[0])
    

    # returns TRUE if we should forward the message and FALSE if we are the closest peer
    def forwardMessage(self, fileLocation):
        peerID = self._ID
        immediateSuccessor = self._immediateSuccessors[0][1][1] - 50000 # ID
        immediatePredecessor = self.findImmediatePredecessor()  # ID
        print("Immediate successor is %d, immediate predecessor is %d"%(immediateSuccessor, immediatePredecessor))
        print(self._immediatePredecessors)
        # cases
        # first check - are we the peer
        if peerID == fileLocation:
            return False # we have the file
        # second check - we are the closest peer
        if immediatePredecessor <= peerID and immediateSuccessor >= peerID: # we are not at start of the DHT
            distances = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor-fileLocation)]
            print("distances from second if is", distances)
            return not(self.closestPeer(distances))
        else:
            distances = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor-fileLocation)]
            if immediateSuccessor < peerID:
                immediateSuccessor = immediateSuccessor + 255
            if immediatePredecessor > peerID:
                peerID = peerID + 255
                print("Peer ID is", peerID)
            distancesModified = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor-fileLocation)]
            print('self id is', self._ID)
            if peerID == self._ID + 255:
                distances = distancesModified.copy()
            if self.closestPeer(distances) and self.closestPeer(distancesModified):
                return False
            return True

    # send a file request message to immediate successor via TCP
    def sendRequestFileMsg(self, requestingPeer, fileLocation, successorLocation, predecessorID, fileID):
        msg = "FILE_REQUEST FILE ID " + str(fileID) + " REQUESTED BY PEER: " +  str(requestingPeer) + " AT LOCATION " + str(fileLocation) + " MESSAGE FORWARDED FROM PEER: " + str(predecessorID)
        self._TCPClientSock.connect((self._IP, successorLocation))
        self._TCPClientSock.send(msg.encode())
        self._TCPClientSock.close()
    
    # listens to incoming TCP connections
    def TCPlisten(self):
        self._TCPServerSock.listen(5)
        print("server sock is", self._TCPServerSock)
        print("Listening for TCP client...")
        while True: 
            conn, clientAddress = self._TCPServerSock.accept()  
            msg = conn.recv(2048) # we use conn - this socket object to communicate to the client, NOT the socket used to listen to the server
            if self.identifyMsg(msg) == "FILE_REQUEST":
                locations = [int(s) for s in msg.split() if s.isdigit()] # extracts the successor location and file location and places them into a list
                self.findFileLocation(locations[0], locations[1], locations[2], locations[3])
            if self.identifyMsg(msg) == "FILE_RESPONSE":
                IDs = [int(s) for s in msg.split() if s.isdigit()]
                print("Received a response message from peer %d, which has the file %d.\n"%(IDs[0], IDs[1]))
            conn.close()
            
    # peer with the file sends a response directly to peer who requested file via TCP        
    def sendFileResponse(self, requestingPeer, fileID):
        msg = "FILE_RESPONSE BY PEER: " + str(self._ID) + " FOR FILE ID: " + str(fileID)
        print("requesting peer is %d, fileID is %d\n"%(requestingPeer, fileID))
        print("attempting to connect to requesting peer", requestingPeer)
        self._TCPClientSock.connect((self._IP, requestingPeer+50000))
        self._TCPClientSock.send(msg.encode())

    def createPacket(self, data, seqNum):
        header = "***HEADER*** SEQ_NUM: " + str(seqNum) + " START"
        #print(header)
        msg = header.encode('utf-8') + data # append header to msg
        return msg

    
    # starts file transfer - might need own thread??
    def sendFile(self, requestingPeer, fileID):
        filename = str(fileID) + str(".pdf")
        f=open(filename,"rb")
        print("We now start sending the file...")
        data = f.read(self._MSS)
        seqNum = 1
        timeout = 1 # in seconds
        addr = ('localhost', requestingPeer + 50000)
        self._UDPSock.sendto("START_TRANSFER".encode(),addr)
        retransmit = False
        wait = True
        while (data):
            if (random.uniform(0,1) > self._dropProb): # we have not dropped the packet, so send it and write the corresponding logfile entry
                msg = self.createPacket(data, seqNum)
                self._UDPSock.sendto(msg, addr) 
                sentTime = time.time()
                print("Sent msg", msg)
                retransmit = False
                wait = True
                while wait == True and time.time()-sentTime < 1:
                    response, clientAddress= self._UDPSock.recvfrom(1024) 
                    print(response)
                    print(self.identifyMsg(response))
                    if self.identifyMsg(response) == "ACK" and ([int(s) for s in response.split() if s.isdigit()][0] == seqNum+len(data)):
                        receivedTime = time.time()
                        print("Advancing buffer")
                        seqNum = seqNum + len(data)
                        data = f.read(self._MSS)
                        wait = False
                    else:
                        print("Msg is not ACK it is:", response)
                if wait == True: # this means we have timed-out
                    retransmitTime = time.time()
                    print("Timeout, starting retransmsision")
                    wait = False
                    retransmit = True
        self._UDPSock.sendto("END_TRANSFER".encode(),addr)
        print("The file is sent...")
        f.close()   
        
    def 
    
    def receiveFile(self): # need to identify that a file transfer is happening
            dec = codecs.getincrementaldecoder('utf8')()
            f = open("received_file.pdf", "wb") # requesting peer opens file
            transferOngoing = True
            while(transferOngoing):
                i = 0
                data, addr = self._UDPSock.recvfrom(4096) # max buffer size??
                if self.identifyMsg(data) == "END_FILE_TRANSFER":
                    print("We have received the file")
                    transferOngoing = False
                    f.close()
                elif self.identifyMsg(data) == "FILE_DATA":
                    print("Message received")
                    recvString = ""
                    while " START" not in recvString:  
                        recvString += dec.decode(data[0:i])
                        i = i+1
                    header = ""
                    header += dec.decode(data[0:i-1])
                    print(header) 
                    headerLength = len(header)
                    msgStart = headerLength
                    #print("msg start is", msgStart)
                    recvString = ""
                    print(data[msgStart:msgStart+int(self._MSS)])
                    f.write(data[msgStart:msgStart+int(self._MSS)]) # need to extract sender MSS so we only write sender's MSS
                    numbers = [int(n) for n in data.split() if n.isdigit()]
                    seqNumber = numbers[0] 
                    ACK = len(data) - msgStart + seqNumber # ACK is the length of the data (not including header) + sequence num
                    ACKmsg = "*****ACK*****: " + str(ACK) + " "
                    print("Sending ACK", ACKmsg)
                    self._UDPSock.sendto(ACKmsg.encode(), addr)
                    sendTime = time.time()
                    print("ACK sent", ACKmsg)
                    

            
    """def extractHeader(self, msg):
        dec = codecs.getincrementaldecoder('utf8')()
        recvString = ""
        i = 0
        while " START" not in recvString:          # finds first index of payload
            recvString += dec.decode(msg[0:i])
            i = i+1
        recvString = ""
        header = ""
        header = msg[0:i-1]
        print(header)
        return (header) 
    
    def findPayload(self, msg): # returns a number corresponding to start of the payload 
        header = self.extractHeader(msg)               
        return len(header)                
    
    def findMSS(self, msg): # returns number corresponding to MSS of sending peer
        header = self.extractHeader(msg)
        headerNums = [int(s) for s in header.split() if s.isdigit()]  # extracts numbers from header
        MSS = headerNums[2]
        return MSS
    """
        
if __name__ == "__main__":
    p1 = Peer(sys.argv[1], sys.argv[4], sys.argv[5])  
    p1.initialiseImmediateSuccessors(sys.argv[2],sys.argv[3])
    p1.bindSock()
    print(p1._immediateSuccessors)
    UDPlisten_thread = threading.Thread(target = p1.UDPlisten, args = ())
    sendPing_thread = threading.Thread(target = p1.sendPingRequest, args = ())
    TCPlisten_thread = threading.Thread(target = p1.TCPlisten, args = ())
    handleFile_thread = threading.Thread(target = p1.handleFileRequest, args = ())
    sendPing_thread.start()
    UDPlisten_thread.start()
    TCPlisten_thread.start()
    handleFile_thread.start()
    sendPing_thread.join()
    UDPlisten_thread.join()
    TCPlisten_thread.join()
    handleFile_thread.start()
 

import sys
import threading
import socket
import time
import re
import codecs
import select
import random

class Peer(object):
    def __init__(self, ID, MSS, dropProb):
        self._ID = int(ID)
        self._MSS = int(MSS) 
        self._port = 50000 + int(ID)
        self._IP = 'localhost'
        self._dropProb = float(dropProb)
        self._immediateSuccessors = [] 
        self._immediatePredecessors = [] 
        self._shutdown = False
        self._UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._TCPServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # end constructor
    
    def bindSock(self):
        self._UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self._UDPSock.bind((self._IP, int(self._port)))
        self._TCPServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._TCPServerSock.bind((self._IP, int(self._port)))
        
    def initialiseImmediateSuccessors(self, successor1, successor2):
        address1 = ('localhost', 50000 + int(successor1))
        address2 = ('localhost', 50000 + int(successor2))
        self._immediateSuccessors.append((successor1, address1))
        self._immediateSuccessors.append((successor2, address2))
      
    # listens to incoming messages, also sends the ping response
    def UDPlisten(self):
        while True:
            try: 
                msg, clientAddress= self._UDPSock.recvfrom(4096)
                clientPort = int(clientAddress[1])-50000
                #if self.identifyMsg(msg) == "PING_RESPONSE":
                    #print("A peer response message was received from Peer %d"%(clientPort))
                if self.identifyMsg(msg) == "PING_REQUEST":
                    self.sendPingResponse(clientAddress) # sending response back to peer
                    self.updatePredecessors(clientPort)
                    #print("A peer request message was received from Peer %d"%(clientPort))
                if self.identifyMsg(msg) == "START_FILE_TRANSFER":
                    print("We now start receiving the file")
                    self.receiveFile()
                #if self.identifyMsg(msg) == "END_FILE_TRANSFER":
                #    print("We have received the file")
                #if self.identifyMsg(msg) == "FILE_TRANSFER":
                #    print("FILE TRANSFER STARTING!!!")
                #    self.receiveFile(msg, clientAddress)
            except KeyboardInterrupt:
                print('Keyboard interrupt, stopping main loop', file=sys.stderr)
                sys.exit(1)

    # determines whether the message is a peer request message, peer response message, a file request/file response message or if the message contains the data of the file transfer
    def identifyMsg(self, msg):
    # need to incrementally decode first 12 bytes - see if PING/FILE in it, if so, decode whole message, if NOT and if ***HEADER** in it, it is file
        dec = codecs.getincrementaldecoder('utf8')()
        identifier = ""
        identifier += dec.decode(msg[0:11])
        if "PING" in identifier:
            msg = msg.decode('utf-8')
            if "PING_REQUEST" in msg:
                #print("ping request")
                return "PING_REQUEST"
            elif "PING_RESPONSE" in msg:
                #print("ping response")
                return "PING_RESPONSE"
        if "FILE" in identifier:
            msg = msg.decode('utf-8')
            if "FILE_REQUEST" in msg:
                return "FILE_REQUEST"
            elif "FILE_RESPONSE" in msg:
                return "FILE_RESPONSE"
        if "START" in identifier:
            msg = msg.decode('utf-8')
            if ("START_TRANSFER") in msg:
                return "START_FILE_TRANSFER"
        if "END" in identifier:
            msg = msg.decode('utf-8')
            if ("END_TRANSFER") in msg:
                return "END_FILE_TRANSFER"
        if "HEADER" in identifier:
            print("file transfer with header")
            return "FILE_DATA"
        if "ACK" in identifier:
            #print("Identifier is", identifier)
            #print("We have an ACK MSG")
            return "ACK"
        
    # sends ping response message to the peer who sent a ping request
    def sendPingResponse(self, clientAddress):
        pingResponse = 'PING_RESPONSE'
        self._UDPSock.sendto(pingResponse.encode(), clientAddress)        
    
    # sends ping request messages to the two immediate successors of a peer to check if they are alive
    def sendPingRequest(self):
        message = 'PING_REQUEST'
        while True:
            time.sleep(2)
            try:
                self._UDPSock.sendto(message.encode(), self._immediateSuccessors[0][1])
                self._UDPSock.sendto(message.encode(), self._immediateSuccessors[1][1])
            except KeyboardInterrupt:
                print("Keyboard interrupt, stopping main loop", file = sys.stderr)
                sys.exit(1)
    
    def updatePredecessors(self, predecessorPort):
        if predecessorPort not in self._immediatePredecessors:
            self._immediatePredecessors.append(predecessorPort)
        self._immediatePredecessors.sort()
        #print("Immediate predecessors are", self._immediatePredecessors)
        
    # applies hash function on fileID to compute location
    def hashFunction(self, fileID):
        return (fileID % 256)

    # handles file requests - continuously waits for input. If input of the form request X, we call the find File Location function
    def handleFileRequest(self):       
        while True:
            userInput = input()
            print(userInput)
            if "request" in userInput:
                fileID = int(re.findall(r'\d+',userInput)[0]) # extracts file ID from input
                print(fileID)
                fileLocation = (self.hashFunction(fileID)) # applies hash function on file ID
                requestingPeer = self._ID
                self.findFileLocation(fileID, requestingPeer, fileLocation, self._ID)
                    
    # determines location of file, we continue calling request file until we are closer to the file's location than our successor - BUG NEED TO KEEP TRACK OF SUCCESSOR AND PREDECESSOR
    def findFileLocation(self, fileID, requestingPeer, fileLocation, predecessorID):
        successorLocation = self._immediateSuccessors[0][1][1]
        successorID = successorLocation - 50000
        peerID = self._ID
        # REMOVE LOGIC FROM THIS SECTION
        if self.forwardMessage(fileLocation) == True:
            print("File %d is not stored here.\n File request message has been forwarded to my successor %d"%(fileLocation, successorID), file = sys.stderr)
            self.sendRequestFileMsg(requestingPeer, fileLocation, successorLocation, predecessorID, fileID)
        else: # we are the closest peer
            print("File %d is here.\n A response message, destined for Peer %d, has been sent.\n"%(fileLocation, requestingPeer), file = sys.stderr)
            self.sendFileResponse(requestingPeer, fileID)
            self.sendFile(requestingPeer, fileID)
            

    # returns true if current peer is closest peer and false otherwise
    def closestPeer(self, distances): 
        if distances[1] <= distances[0] and distances[1] <= distances[2]: # that means we are the closest peer
            print("Returning true")
            return True
        print("Returning false")
        return False

    def findImmediatePredecessor(self):
        peerID = self._ID
        if self._immediatePredecessors[1] <= peerID:
            return int(self._immediatePredecessors[1])
        else:
            return int(self._immediatePredecessors[0])
    

    # returns TRUE if we should forward the message and FALSE if we are the closest peer
    def forwardMessage(self, fileLocation):
        peerID = self._ID
        immediateSuccessor = self._immediateSuccessors[0][1][1] - 50000 # ID
        immediatePredecessor = self.findImmediatePredecessor()  # ID
        print("Immediate successor is %d, immediate predecessor is %d"%(immediateSuccessor, immediatePredecessor))
        print(self._immediatePredecessors)
        # cases
        # first check - are we the peer
        if peerID == fileLocation:
            return False # we have the file
        # second check - we are the closest peer
        if immediatePredecessor <= peerID and immediateSuccessor >= peerID: # we are not at start of the DHT
            distances = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor-fileLocation)]
            print("distances from second if is", distances)
            return not(self.closestPeer(distances))
        else:
            distances = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor-fileLocation)]
            if immediateSuccessor < peerID:
                immediateSuccessor = immediateSuccessor + 255
            if immediatePredecessor > peerID:
                peerID = peerID + 255
                print("Peer ID is", peerID)
            distancesModified = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor-fileLocation)]
            print('self id is', self._ID)
            if peerID == self._ID + 255:
                distances = distancesModified.copy()
            if self.closestPeer(distances) and self.closestPeer(distancesModified):
                return False
            return True

    # send a file request message to immediate successor via TCP
    def sendRequestFileMsg(self, requestingPeer, fileLocation, successorLocation, predecessorID, fileID):
        msg = "FILE_REQUEST FILE ID " + str(fileID) + " REQUESTED BY PEER: " +  str(requestingPeer) + " AT LOCATION " + str(fileLocation) + " MESSAGE FORWARDED FROM PEER: " + str(predecessorID)
        self._TCPClientSock.connect((self._IP, successorLocation))
        self._TCPClientSock.send(msg.encode())
        self._TCPClientSock.close()
    
    # listens to incoming TCP connections
    def TCPlisten(self):
        self._TCPServerSock.listen(5)
        print("server sock is", self._TCPServerSock)
        print("Listening for TCP client...")
        while True: 
            conn, clientAddress = self._TCPServerSock.accept()  
            msg = conn.recv(2048) # we use conn - this socket object to communicate to the client, NOT the socket used to listen to the server
            if self.identifyMsg(msg) == "FILE_REQUEST":
                locations = [int(s) for s in msg.split() if s.isdigit()] # extracts the successor location and file location and places them into a list
                self.findFileLocation(locations[0], locations[1], locations[2], locations[3])
            if self.identifyMsg(msg) == "FILE_RESPONSE":
                IDs = [int(s) for s in msg.split() if s.isdigit()]
                print("Received a response message from peer %d, which has the file %d.\n"%(IDs[0], IDs[1]))
            conn.close()
            
    # peer with the file sends a response directly to peer who requested file via TCP        
    def sendFileResponse(self, requestingPeer, fileID):
        msg = "FILE_RESPONSE BY PEER: " + str(self._ID) + " FOR FILE ID: " + str(fileID)
        print("requesting peer is %d, fileID is %d\n"%(requestingPeer, fileID))
        print("attempting to connect to requesting peer", requestingPeer)
        self._TCPClientSock.connect((self._IP, requestingPeer+50000))
        self._TCPClientSock.send(msg.encode())

    def createPacket(self, data, seqNum):
        header = "***HEADER*** SEQ_NUM: " + str(seqNum) + " START"
        #print(header)
        msg = header.encode('utf-8') + data # append header to msg
        return msg

    
    # starts file transfer - might need own thread??
    def sendFile(self, requestingPeer, fileID):
        filename = str(fileID) + str(".pdf")
        f=open(filename,"rb")
        print("We now start sending the file...")
        data = f.read(self._MSS)
        seqNum = 1
        timeout = 1 # in seconds
        addr = ('localhost', requestingPeer + 50000)
        self._UDPSock.sendto("START_TRANSFER".encode(),addr)
        retransmit = False
        wait = True
        while (data):
            if (random.uniform(0,1) > self._dropProb): # we have not dropped the packet, so send it and write the corresponding logfile entry
                msg = self.createPacket(data, seqNum)
                self._UDPSock.sendto(msg, addr) 
                sentTime = time.time()
                print("Sent msg", msg)
                retransmit = False
                wait = True
                while wait == True and time.time()-sentTime < 1:
                    response, clientAddress= self._UDPSock.recvfrom(1024) 
                    print(response)
                    print(self.identifyMsg(response))
                    if self.identifyMsg(response) == "ACK" and ([int(s) for s in response.split() if s.isdigit()][0] == seqNum+len(data)):
                        receivedTime = time.time()
                        print("Advancing buffer")
                        seqNum = seqNum + len(data)
                        data = f.read(self._MSS)
                        wait = False
                    else:
                        print("Msg is not ACK it is:", response)
                if wait == True: # this means we have timed-out
                    retransmitTime = time.time()
                    print("Timeout, starting retransmsision")
                    wait = False
                    retransmit = True
        self._UDPSock.sendto("END_TRANSFER".encode(),addr)
        print("The file is sent...")
        f.close()   
        
    def 
    
    def receiveFile(self): # need to identify that a file transfer is happening
            dec = codecs.getincrementaldecoder('utf8')()
            f = open("received_file.pdf", "wb") # requesting peer opens file
            transferOngoing = True
            while(transferOngoing):
                i = 0
                data, addr = self._UDPSock.recvfrom(4096) # max buffer size??
                if self.identifyMsg(data) == "END_FILE_TRANSFER":
                    print("We have received the file")
                    transferOngoing = False
                    f.close()
                elif self.identifyMsg(data) == "FILE_DATA":
                    print("Message received")
                    recvString = ""
                    while " START" not in recvString:  
                        recvString += dec.decode(data[0:i])
                        i = i+1
                    header = ""
                    header += dec.decode(data[0:i-1])
                    print(header) 
                    headerLength = len(header)
                    msgStart = headerLength
                    #print("msg start is", msgStart)
                    recvString = ""
                    print(data[msgStart:msgStart+int(self._MSS)])
                    f.write(data[msgStart:msgStart+int(self._MSS)]) # need to extract sender MSS so we only write sender's MSS
                    numbers = [int(n) for n in data.split() if n.isdigit()]
                    seqNumber = numbers[0] 
                    ACK = len(data) - msgStart + seqNumber # ACK is the length of the data (not including header) + sequence num
                    ACKmsg = "*****ACK*****: " + str(ACK) + " "
                    print("Sending ACK", ACKmsg)
                    self._UDPSock.sendto(ACKmsg.encode(), addr)
                    sendTime = time.time()
                    print("ACK sent", ACKmsg)
                    

            
    """def extractHeader(self, msg):
        dec = codecs.getincrementaldecoder('utf8')()
        recvString = ""
        i = 0
        while " START" not in recvString:          # finds first index of payload
            recvString += dec.decode(msg[0:i])
            i = i+1
        recvString = ""
        header = ""
        header = msg[0:i-1]
        print(header)
        return (header) 
    
    def findPayload(self, msg): # returns a number corresponding to start of the payload 
        header = self.extractHeader(msg)               
        return len(header)                
    
    def findMSS(self, msg): # returns number corresponding to MSS of sending peer
        header = self.extractHeader(msg)
        headerNums = [int(s) for s in header.split() if s.isdigit()]  # extracts numbers from header
        MSS = headerNums[2]
        return MSS
    """
        
if __name__ == "__main__":
    p1 = Peer(sys.argv[1], sys.argv[4], sys.argv[5])  
    p1.initialiseImmediateSuccessors(sys.argv[2],sys.argv[3])
    p1.bindSock()
    print(p1._immediateSuccessors)
    UDPlisten_thread = threading.Thread(target = p1.UDPlisten, args = ())
    sendPing_thread = threading.Thread(target = p1.sendPingRequest, args = ())
    TCPlisten_thread = threading.Thread(target = p1.TCPlisten, args = ())
    handleFile_thread = threading.Thread(target = p1.handleFileRequest, args = ())
    sendPing_thread.start()
    UDPlisten_thread.start()
    TCPlisten_thread.start()
    handleFile_thread.start()
    sendPing_thread.join()
    UDPlisten_thread.join()
    TCPlisten_thread.join()
    handleFile_thread.start()
 


