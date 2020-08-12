import sys
import threading
import socket
import time
import re
import codecs
import select
import random
from multiprocessing.pool import Pool
import ctypes

# LATER ON: 
# DATA SPLIT FOR IDENTIFIERS
# NEED TO DEAL WITH DUPLICATES (DUPLICATE PACKETS IN CASE ACK DROPPED) - done
# step 4: need to deal with 1 peer remaining in network - update successors
# NEED TO REMOVE DEAD PEERS FROM SUCCESSORS
# CASE WHERE ONE PEER LEFT ALL OTHERS HAVE DEPARTED - remove DEAD PEERS FROM SUCCESSORS


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
        self._UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self._TCPServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self._TCPServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._fileSenderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._fileReceiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    # end constructor
    
    def bindSock(self):
        self._UDPSock.bind((self._IP, int(self._port)))
        self._TCPServerSock.bind((self._IP, int(self._port)))
        self._fileReceiverSock.bind((self._IP, int(self._port)+500))
        
    def initialiseImmediateSuccessors(self, successor1, successor2):
        address1 = ('localhost', 50000 + int(successor1))
        address2 = ('localhost', 50000 + int(successor2))
        if int(successor1) != self._ID and int(successor1) != int(successor2):  
            self._immediateSuccessors.append((int(successor1), address1))
        if successor2 != self._ID and successor2 != successor1: 
            self._immediateSuccessors.append((int(successor2), address2))
        
    # listens to incoming messages, also sends the ping response
    def UDPlisten(self):
        succ1ACK = 0
        succ2ACK = 0
        succ1MissedACKs = 0
        succ2MissedACKs = 0
        while True:
            try: 
                msg, clientAddress = self._UDPSock.recvfrom(4096)
                #print("Successors are", self._immediateSuccessors)
                if succ1MissedACKs > 5:
                    killedPeer = int(self._immediateSuccessors[0][0])
                    print("\n***Peer %d is no longer alive***\n"%(killedPeer))
                    while int(self._immediateSuccessors[0][0]) == killedPeer:
                        successor1 = int(self._immediateSuccessors[1][0])
                        #print("Successor 1 is %d", int(successor1))
                        self.sendFindSuccessorMsg(successor1)
                        succ1ACK = succ2ACK
                        succ2ACK = pingSeqNum # successor 2's last ACK = seqNum (so not automatically declared as dead)
                    print("\n***My first successor is now Peer %d.\nMy second successor is now Peer %d***\n"%(int(self._immediateSuccessors[0][0]), int(self._immediateSuccessors[1][0])))
                if succ2MissedACKs > 5:
                    killedPeer = int(self._immediateSuccessors[1][0])
                    print("\n***Peer %d is no longer alive***\n"%(killedPeer))
                    while int(self._immediateSuccessors[1][0]) == killedPeer:
                        successor1 = int(self._immediateSuccessors[0][0])
                        self.sendFindSuccessorMsg(successor1)
                        succ2ACK = pingSeqNum
                    print("\n***My first successor is now Peer %d.\nMy second successor is now Peer %d***\n"%(int(self._immediateSuccessors[0][0]), int(self._immediateSuccessors[1][0])))
                if self.identifyMsg(msg) == "PING_RESPONSE":
                    clientID = [int(n) for n in msg.split() if n.isdigit()][0]
                    ACKNum = [int(n) for n in msg.split() if n.isdigit()][1]
                    if clientID == int(self._immediateSuccessors[0][0]): # this means the peer responding is our first successor
                        succ1ACK = ACKNum
                    elif clientID == int(self._immediateSuccessors[1][0]):
                        succ2ACK = ACKNum
                    print("A ping response message was received from Peer %d."%(clientID))
                if self.identifyMsg(msg) == "PING_REQUEST":
                    clientID = [int(n) for n in msg.split() if n.isdigit()][0]
                    print("A ping request message was received from Peer %d."%(clientID))
                    self.sendPingResponse(clientID, msg) # sending response back to peer
                    self.updatePredecessors(clientID)
                succ1MissedACKs = pingSeqNum - succ1ACK
                succ2MissedACKs = pingSeqNum - succ2ACK
                #print("Succ1 Missed ACKs is %d succ2 missed ACKs is %d"%(succ1MissedACKs, succ2MissedACKs))
            except KeyboardInterrupt:
                self.terminateThread(UDPlisten_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPlisten_thread)
                self.terminateThread(handleFile_thread)
                os._exit(0)

    # determines whether the message is a peer request message, peer response message, a file request/file response message or if the message contains the data of the file transfer
    def identifyMsg(self, msg):
    # need to incrementally decode first 12 bytes - see if PING/FILE in it, if so, decode whole message, if NOT and if ***HEADER** in it, it is file
        dec = codecs.getincrementaldecoder('utf8')()
        identifier = ""
        identifier += dec.decode(msg[0:10])
        if "PING" in identifier:
            msg = msg.decode('utf-8')
            if "PING_REQUEST" in msg:
                return "PING_REQUEST"
            elif "PING_RESPONSE" in msg:
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
            return "FILE_DATA"
        if "ACK" in identifier:
            return "ACK"
        if "DEPARTURE" in identifier:
            return "GRACEFUL_DEPARTURE"
        if "FIND" in identifier:
            return "FIND_SUCCESSOR"
        if "HAVE" in identifier:
            return "HAVE_SUCCESSOR"
        
    # sends ping response message to the peer who sent a ping request with corresponding sequence number
    def sendPingResponse(self, clientID, msg):
        pingResponse = 'PING_RESPONSE '
        seqNum = [int(n) for n in msg.split() if n.isdigit()][1]
        pingResponse = "PING_RESPONSE " + "FROM ID: " + str(self._ID) + " SEQUENCE NUMBER: " + str(seqNum)
        self._UDPSock.sendto(pingResponse.encode(), ('localhost', clientID + 50000))        
    
    # potentially might need a ping monitor thread
    # ping monitor thread needs to keep track of both what ping requests are being sent and what ping responses have been received
    
    # sends ping request messages to the two immediate successors of a peer to check if they are alive. Ping request has a sequence number
    # invoke thread in UDPlisten & pass in an argument ?? the sequence number??
    def sendPingRequest(self):
        global pingSeqNum
        pingSeqNum = 0
        while True:
            #print("sending ping")
            time.sleep(7)
            message = 'PING_REQUEST FROM SENDER ' + str(self._ID) + " SEQUENCE NUMBER " + str(pingSeqNum)
            try:
                if len(self._immediateSuccessors) == 2:
                    self._UDPSock.sendto(message.encode(), self._immediateSuccessors[0][1])
                    self._UDPSock.sendto(message.encode(), self._immediateSuccessors[1][1])
                if len(self._immediateSuccessors) == 1:
                    self._UDPSock.sendto(message.encode(), self._immediateSuccessors[0][1])
                #print("PingSeqNum is sendping request is %d"%(pingSeqNum))
                pingSeqNum = pingSeqNum + 1
            except KeyboardInterrupt:
                self.terminateThread(UDPlisten_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPlisten_thread)
                self.terminateThread(handleFile_thread)
                os._exit(0)
        
        
    def updatePredecessors(self, predecessorPort):
        if len(self._immediatePredecessors) == 3:
            self._immediatePredecessors.clear()
        if predecessorPort not in self._immediatePredecessors:
            self._immediatePredecessors.append(predecessorPort)
        self.orderPredecessors() # order predecessors
        #print("Predecessors are", self._immediatePredecessors)
        
    def orderPredecessors(self):
        self._immediatePredecessors.sort()
        if len(self._immediatePredecessors) >= 2:
            if self._ID > self._immediatePredecessors[1]:
                immediatePredecessor = self._immediatePredecessors[1]
                secondPredecessor = self._immediatePredecessors[0]
                self._immediatePredecessors[0] = immediatePredecessor
                self._immediatePredecessors[1] = secondPredecessor
            
    
    # applies hash function on fileID to compute location
    def hashFunction(self, fileID):
        return (fileID % 256)

    # handles file requests - continuously waits for input. If input of the form request X, we call the find File Location function
    def handleFileRequest(self):       
        try:
            while True:
                userInput = input()
                if "request" in userInput:
                    fileID = int(re.findall(r'\d+',userInput)[0]) # extracts file ID from input
                    fileLocation = (self.hashFunction(fileID)) # applies hash function on file ID
                    requestingPeer = self._ID
                    self.findFileLocation(fileID, requestingPeer, fileLocation, self._ID)
                elif "quit" in userInput:
                    self.sendPeerChurnMsg()
                    self.terminateThread(UDPlisten_thread)
                    self.terminateThread(sendPing_thread)
                    self.terminateThread(TCPlisten_thread)
                    self.terminateThread(handleFile_thread)
                    # kill threads / close socket
                    sys.exit(1) # maybe need to manage threads??
        except KeyboardInterrupt:
                self.terminateThread(UDPlisten_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPlisten_thread)
                self.terminateThread(handleFile_thread)
                # kill threads / close socket
                os._exit(0)
                  
    # by By Johan Dahlin (http://stackoverflow.com/a/15274929/1800854)
    
    def terminateThread(self, thread):
        if not thread.isAlive():
            return
        exc = ctypes.py_object(SystemExit);
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc);
        if res == 0:
            raise ValueError("nonexistent thread id");
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None);
            raise SystemError("PyThreadState_SetAsyncExc failed");

     
    def sendPeerChurnMsg(self):
        try: # if we have more than two immediate predecessors, send properly. if we do not, send to our only successor that we will be leaving
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## NEED TO CHANGE IMMEDIATE PREDECESSORS SO NOT ORDERED BY MAX IN CASE WE ARE AT FIRST PART
            sock1.connect((self._IP, self._immediatePredecessors[1]+50000))
            msg1 = "DEPARTURE OF PEER " + str(self._ID) + " ONE UPDATE OF SECOND SUCCESSOR TO " + str(self._immediateSuccessors[0][0])
            sock1.send(msg1.encode())
            #print("Sending msg1 %s to peer %d at port %d"%(msg1, self._immediatePredecessors[1], self._immediatePredecessors[1] + 50000))
            sock1.close()
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.connect((self._IP, self._immediatePredecessors[0]+50000));
            if len(self._immediateSuccessors) >= 2:
                msg2 = "DEPARTURE OF PEER " + str(self._ID) + " TWO UPDATES: FIRST SUCCESSOR TO " + str(self._immediateSuccessors[0][0]) + " SECOND SUCCESSOR TO " + str(self._immediateSuccessors[1][0])
                #print("Sending msg2 %s to peer %d at port %d"%(msg2, self._immediatePredecessors[0], self._immediatePredecessors[0] + 50000))      
                sock2.send(msg2.encode())
                sock2.close()
        except socket.error:
            pass
        
    def sendFindSuccessorMsg(self, successor1):
        try:
            # send over TCP
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.connect((self._IP, int(successor1) + 50000))
            msg = "FIND IMMEDIATE SUCCESSOR REQUEST FROM PEER " + str(self._ID) + " WITH FIRST SUCCESSOR " + str(successor1)
            sock1.send(msg.encode())
            sock1.close()
        except socket.error:
            pass
    
    def sendImmediateSuccessorMsg(self, requesterID, successor1):
        try:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.connect((self._IP, int(requesterID) + 50000))
            msg = "HAVE FIRST SUCCESSOR " + str(successor1) + " SECOND SUCCESSOR AS REQUESTED: " + str(self._immediateSuccessors[0][0])
            sock1.send(msg.encode())
            sock1.close()
        except socket.error:
            pass
    
    # determines location of file, we continue calling request file until we are closer to the file's location than our successor - BUG NEED TO KEEP TRACK OF SUCCESSOR AND PREDECESSOR
    def findFileLocation(self, fileID, requestingPeer, fileLocation, predecessorID):
        successorLocation = int(self._immediateSuccessors[0][1][1])
        successorID = successorLocation - 50000
        peerID = self._ID
        if self.forwardMessage(fileLocation) == True:
            print("\n***File %d is not stored here.***\n***File request message has been forwarded to my successor %d.***\n"%(fileLocation, successorID), file = sys.stderr)
            self.sendRequestFileMsg(requestingPeer, fileLocation, successorLocation, predecessorID, fileID)
        else: # we are the closest peer
            print("\n***File %d is here.***\n***A response message, destined for Peer %d, has been sent.***\n"%(fileLocation, requestingPeer), file = sys.stderr)
            self.sendFileResponse(requestingPeer, fileID)
            self.sendFile(requestingPeer, fileID)
            

    # returns true if next peer is closest peer and false otherwise
    def forwardtoSuccessor(self, distances): 
        if distances[2] <= distances[1] and distances[2] <= distances[1]: # that means we should forward
            #print("Should forward to successor with distances", distances)
            return True
        elif distances[0] <= distances[1] and distances[0] <= distances[2]:
            #print("Should forward to successor with distances", distances)
            return True
        #print("Shouldn't forward to successor with distances", distances)
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
        immediateSuccessor = int(self._immediateSuccessors[0][1][1]) - 50000 # ID
        immediatePredecessor = self.findImmediatePredecessor()
        #print("Immediate successor is %d, immediate predecessor is %d"%(immediateSuccessor, immediatePredecessor))
        if fileLocation == self._ID:
            return False
        distances = [abs(immediatePredecessor-fileLocation), abs(peerID - fileLocation), abs(immediateSuccessor-fileLocation)]
        if immediateSuccessor > peerID and immediatePredecessor < peerID: # non-wrap around case
            #print("Peer is %d, immediate successor is %d, immediate predecessor is %d"%(peerID, immediateSuccessor, immediatePredecessor))
            if self.forwardtoSuccessor(distances) == True:
                return True
        if immediateSuccessor < peerID: # just about to come full-circle
            modifiedDistances = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor+255-fileLocation)]
            #print("Distances are", distances)
            #print("Modified distances are", modifiedDistances)
            if self.forwardtoSuccessor(modifiedDistances) == True:
                return True
            elif self.forwardtoSuccessor(distances) == True:
                return True
            return False
        if immediatePredecessor > peerID: # at start of DHT    
            modifiedDistances = [abs(immediatePredecessor-fileLocation), abs(peerID+255-fileLocation), abs(immediateSuccessor-fileLocation)]
            if self.forwardtoSuccessor(modifiedDistances) == False:
                return False
            if self.forwardtoSuccessor(distances) == True:
                return True
            return False

    # send a file request message to immediate successor via TCP
    def sendRequestFileMsg(self, requestingPeer, fileLocation, successorLocation, predecessorID, fileID):
        msg = "FILE_REQUEST FILE ID " + str(fileID) + " REQUESTED BY PEER: " +  str(requestingPeer) + " AT LOCATION " + str(fileLocation) + " MESSAGE FORWARDED FROM PEER: " + str(predecessorID)
        self._TCPClientSock.connect((self._IP, successorLocation))
        self._TCPClientSock.send(msg.encode())
        self._TCPClientSock.close()
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # listens to incoming TCP connections
    def TCPlisten(self):
        self._TCPServerSock.listen(5)
        #print("server sock is", self._TCPServerSock)
        #print("Listening for TCP client...")
        while True: 
            try:
                conn, clientAddress = self._TCPServerSock.accept()  
                msg = conn.recv(2048) # we use conn - this socket object to communicate to the client, NOT the socket used to listen to the server
                if self.identifyMsg(msg) == "FILE_REQUEST":
                    locations = [int(s) for s in msg.split() if s.isdigit()] # extracts the successor location and file location and places them into a list
                    self.findFileLocation(locations[0], locations[1], locations[2], locations[3])
                if self.identifyMsg(msg) == "FILE_RESPONSE":
                    IDs = [int(s) for s in msg.split() if s.isdigit()]
                    print("\n***Received a response message from peer %d, which has the file %d.***\n"%(IDs[0], IDs[1]))
                conn.close()
                if self.identifyMsg(msg) == "GRACEFUL_DEPARTURE":
                    departingPeer = [int(s) for s in msg.split() if s.isdigit()][0]
                    successors = [int(s) for s in msg.split() if s.isdigit()][1:]
                    print("\n***Peer %d will depart the network***\n" %(departingPeer))
                    if "ONE UPDATE" in msg.decode(): # only need to update one of the successors
                        firstSuccessor = int(self._immediateSuccessors[0][0])
                        self._immediateSuccessors.clear()
                        self.initialiseImmediateSuccessors(firstSuccessor, successors[0])
                        #print("New successors are", self._immediateSuccessors)
                    else: # update two successors - MIGHT NEED TO CHANGE THIS
                        self._immediateSuccessors.clear()
                        self.initialiseImmediateSuccessors(successors[0], successors[1])
                    print("\n***My first successor is now Peer %d.***\n***My second successor is now Peer %d.***\n"%(int(self._immediateSuccessors[0][0]), int(self._immediateSuccessors[1][0])))
                if self.identifyMsg(msg) == "FIND_SUCCESSOR":
                    #print("Received a request to find successor", msg)
                    requesterID = [int(s) for s in msg.split() if s.isdigit()][0]
                    successor1 = [int(s) for s in msg.split() if s.isdigit()][1]
                    self.sendImmediateSuccessorMsg(requesterID, successor1)
                    # send successor to TCP location
                if self.identifyMsg(msg) == "HAVE_SUCCESSOR": 
                    #print("Received a message with successor", msg)
                    successor1 = [int(s) for s in msg.split() if s.isdigit()][0]
                    successor2 = [int(s) for s in msg.split() if s.isdigit()][1]
                    #print("Successor 1 is %d successor 2 is %d"%(successor1, successor2))
                    self._immediateSuccessors.clear()
                    self.initialiseImmediateSuccessors(successor1, successor2)
            except KeyboardInterrupt:
                self.terminateThread(UDPlisten_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPlisten_thread)
                self.terminateThread(handleFile_thread)
                os._exit(0)  

    # peer with the file sends a response directly to peer who requested file via TCP        
    def sendFileResponse(self, requestingPeer, fileID):
        msg = "FILE_RESPONSE BY PEER: " + str(self._ID) + " FOR FILE ID: " + str(fileID)
        #print("requesting peer is %d, fileID is %d\n"%(requestingPeer, fileID))
        #print("attempting to connect to requesting peer", requestingPeer)
        self._TCPClientSock.connect((self._IP, requestingPeer+50000))
        self._TCPClientSock.send(msg.encode())
        self._TCPClientSock.close()
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def createPacket(self, data, ISN, seqNum):
        header = "***HEADER*** ISN: " + str(ISN) + " SEQ_NUM: " + str(seqNum) + " MSS: " + str(self._MSS) + " START"
        msg = header.encode('utf-8') + data # append header to msg
        return msg


    def createLogEntrySender(self, retransmit, drop, time, seqNum, dataLen, ACKNum, send):
        if send == True:
            if drop == True:
                if retransmit == True:
                    logEntry = "Type of message: RTX/Drop \t" + "Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(dataLen) + "\t" + "ACK num: " + str(0) + "\n"
                else:
                    logEntry = "Type of message: Drop \t" +"Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(dataLen) + "\t" + "ACK num: " + str(0) +"\n"
            elif drop == False:
                if retransmit == True:
                    logEntry = "Type of message: RTX \t" + "Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(dataLen) + "\t" + "ACK num: " + str(0) + "\n"   
                else: 
                    logEntry = "Type of message: snd \t" + "Time: " + str("%.2f"%time) + "\t"+ "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(dataLen) + "\t" + "ACK num: " + str(0) + "\n"
        else:
            logEntry = "Type of message: Recv \t" + "Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(0) + "\t" + "Data size: " + str(dataLen) + "\t" + "ACK num: " + str(ACKNum) + "\n"
        return logEntry
    
    def createLogEntryReceiver(self, receive, time, seqNumber, ACK):
        if receive == True:
            logEntry = "Type of message: recv \t" + "Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(seqNumber) + "\t" + "Data size: " + str(ACK-seqNumber) + "\t" + "ACK num: " + str(0) + "\n"
        else:
            logEntry = "Type of message: Send \t" + "Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(0) + "\t" + "Data size: " + str(ACK-seqNumber) + "\t" + "ACK num: " + str(ACK) + "\n"
        return logEntry
    
    
    def fileReceiverListen(self):
        while True:
            try: 
                msg, clientAddress= self._fileReceiverSock.recvfrom(4096)
                if self.identifyMsg(msg) == "START_FILE_TRANSFER":
                    fileID = [int(n) for n in msg.split() if n.isdigit()][0]
                    print("\n***We now start receiving the file***\n")
                    self.receiveFile(fileID)
            except KeyboardInterrupt:
                self.terminateThread(UDPlisten_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPlisten_thread)
                self.terminateThread(handleFile_thread)
                os._exit(0)   
    
    # starts file transfer 
    def sendFile(self, requestingPeer, fileID): 
        filename = str(fileID) + str(".pdf")
        f=open(filename,"rb")
        logfilename = "sender_log" + "_" + str(fileID) + "_" + str(requestingPeer) + ".txt"
        logfile = open(logfilename, "w+")
        print("\n***We now start sending the file...***\n")
        data = f.read(self._MSS)
        ISN = random.randint(1,999)
        seqNum = ISN
        addr = ('localhost', requestingPeer + 60000)
        #print("Requesting peer + 60000 is %d"%(requestingPeer + 60000))
        msg = "START_TRANSFER OF FILE " + str(fileID) 
        self._fileSenderSock.sendto(msg.encode(),('localhost',requestingPeer+50500))
        retransmit = False
        wait = True
        timeout = 1
        while (data):
            wait = True
            if (random.uniform(0,1) > self._dropProb): # we have not dropped the packet, so send it and write the corresponding logfile entry
                msg = self.createPacket(data, ISN, seqNum)
                self._fileSenderSock.sendto(msg, addr) 
                sendTime = time.time()
                if retransmit == True:
                    logfile.write(self.createLogEntrySender(retransmit, False, sendTime, seqNum, len(data), None, True))
                else:
                    logfile.write(self.createLogEntrySender(retransmit, False, sendTime, seqNum, len(data), None, True))
            else: # we have dropped packet
                dropTime = time.time()
                if retransmit == True:
                    logfile.write(self.createLogEntrySender(retransmit, True, dropTime, seqNum, len(data), None, True))
                else:
                    logfile.write(self.createLogEntrySender(retransmit, True, dropTime, seqNum, len(data), None, True))          
            retransmit = False
            wait = True
            while wait == True:
                ready = select.select([self._fileSenderSock],[],[],timeout)
                try: 
                    if ready[0]:
                        receivedTime = time.time()
                        response, clientAddress = self._fileSenderSock.recvfrom(4096)
                        #print("Response in file transfer is", response) 
                        if "ACK" in response.decode():
                            receivedACK = [int(s) for s in response.split() if s.isdigit()][0]
                            if receivedACK == seqNum+len(data):
                                logfile.write(self.createLogEntrySender(None, None, receivedTime, str(0), len(data), receivedACK, False)) # write recv log entry
                                #print("Advancing buffer")
                                seqNum = seqNum + len(data)
                                data = f.read(self._MSS)
                                wait = False
                    else: 
                        #print("TIMEOUT, starting retransmsision")
                        wait = False
                        retransmit = True
                except KeyboardInterrupt:
                    self.terminateThread(UDPlisten_thread)
                    self.terminateThread(sendPing_thread)
                    self.terminateThread(TCPlisten_thread)
                    self.terminateThread(handleFile_thread)
                    os._exit(0)
        self._UDPSock.sendto("END_TRANSFER".encode(),addr)
        print("\n***The file is sent...***\n")
        f.close()   
        
    
    # also deals with duplicate messages in the very rare case the ACK does not get sent successfully to the receiver 
    def receiveFile(self, fileID): 
            dec = codecs.getincrementaldecoder('utf8')()
            receivingSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            receivingSock.bind((self._IP, int(self._port) + 10000))
            filename = "received_file" + "_" + str(fileID) + "_" + str(self._ID) + ".pdf"
            f = open(filename, "wb") # requesting peer opens file
            logfilename = "receiver_log" + "_" + str(fileID) + "_" + str(self._ID) + ".txt"
            logfile = open(logfilename, "w+")
            transferOngoing = True
            while(transferOngoing):
                i = 0
                data, addr = receivingSock.recvfrom(4096) # max buffer size??
                receiveTime = time.time()
                if self.identifyMsg(data) == "END_FILE_TRANSFER":
                    print("\n***We have received the file***\n")
                    f.close()
                    transferOngoing = False
                elif self.identifyMsg(data) == "FILE_DATA":
                    recvString = ""
                    while " START" not in recvString:  
                        recvString += dec.decode(data[0:i])
                        i = i+1
                    header = ""
                    header += dec.decode(data[0:i-1])
                    headerLength = len(header)
                    msgStart = headerLength
                    #print("msg start is", msgStart)
                    recvString = ""
                    numbers = [int(n) for n in header.split() if n.isdigit()]
                    ISN = numbers[0]
                    seqNumber = numbers[1] 
                    MSS = numbers[2]
                    ACK = len(data) - msgStart + seqNumber # ACK is the length of the data (not including header) + sequence num
                    if seqNumber == ISN:
                        seqNumOld = ISN
                    # only want to write to file if we have not seen the packet before
                    if seqNumOld != seqNumber:
                        logfile.write(self.createLogEntryReceiver(True, receiveTime, seqNumber, ACK))
                    #print(data[msgStart:msgStart+MSS])
                    f.write(data[msgStart:msgStart+MSS]) # need to extract sender MSS so we only write sender's MSS
                    ACKmsg = "*****ACK*****: " + str(ACK) + " "
                    #print("Sending ACK", ACKmsg)
                    receivingSock.sendto(ACKmsg.encode(), addr)
                    sendTime = time.time()
                    logfile.write(self.createLogEntryReceiver(False, sendTime, seqNumber, ACK))
                    #print("ACK sent", ACKmsg)
                    seqNumOld = seqNumber
                    

        
if __name__ == "__main__":
    p1 = Peer(sys.argv[1], sys.argv[4], sys.argv[5])  
    p1.initialiseImmediateSuccessors(sys.argv[2],sys.argv[3])
    p1.bindSock()
    UDPlisten_thread = threading.Thread(target = p1.UDPlisten, args = ())
    sendPing_thread = threading.Thread(target = p1.sendPingRequest, args = ())
    TCPlisten_thread = threading.Thread(target = p1.TCPlisten, args = ())
    handleFile_thread = threading.Thread(target = p1.handleFileRequest, args = ())
    fileReceiverListen_thread = threading.Thread(target = p1.fileReceiverListen, args = ())
    sendPing_thread.daemon = True
    UDPlisten_thread.daemon = True
    TCPlisten_thread.daemon = True
    handleFile_thread.daemon = True
    fileReceiverListen_thread.daemon = True
    sendPing_thread.start()
    UDPlisten_thread.start()
    TCPlisten_thread.start()
    handleFile_thread.start()
    fileReceiverListen_thread.start()
    sendPing_thread.join()
    UDPlisten_thread.join()
    TCPlisten_thread.join()
    handleFile_thread.join()
    fileReceiverListen_thread.join()

    


