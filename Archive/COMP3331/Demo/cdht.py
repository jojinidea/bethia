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
import os

class Peer(object):
    def __init__(self, ID, MSS, dropProb):
        self._ID = int(ID)
        self._MSS = int(MSS) 
        self._port = 50000 + int(ID) 
        self._IP = 'localhost'
        self._dropProb = float(dropProb)
        self._immediateSuccessors = [] 
        self._immediatePredecessors = [] 
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
        self._fileReceiverSock.bind((self._IP, int(self._port) + 10000))
        
    def initialiseImmediateSuccessors(self, successor1, successor2):
        address1 = ('localhost', 50000 + int(successor1))
        address2 = ('localhost', 50000 + int(successor2))
        if int(successor1) != self._ID and int(successor1) != int(successor2):  
            self._immediateSuccessors.append((int(successor1), address1))
        if successor2 != self._ID and successor2 != successor1: 
            self._immediateSuccessors.append((int(successor2), address2))
        
    # listens to incoming messages, also sends the ping response
    def UPDListen(self):
        succ1ACK = 0
        succ2ACK = 0
        succ1MissedACKs = 0
        succ2MissedACKs = 0
        while True:
            try: 
                msg, clientAddress = self._UDPSock.recvfrom(4096)
                if succ1MissedACKs >= 7:
                    killedPeer = int(self._immediateSuccessors[0][0])
                    print("\n***Peer %d is no longer alive***\n"%(killedPeer))
                    while int(self._immediateSuccessors[0][0]) == killedPeer:
                        successor1 = int(self._immediateSuccessors[1][0])
                        self.sendFindSuccessorMsg(successor1)
                        succ1ACK = succ2ACK
                        succ2ACK = pingSeqNum # successor 2's last ACK = seqNum (so not automatically declared as dead)
                    print("\n***My first successor is now Peer %d.\nMy second successor is now Peer %d***\n"%(int(self._immediateSuccessors[0][0]), int(self._immediateSuccessors[1][0])))
                if succ2MissedACKs >= 7:
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
                    if clientID == int(self._immediateSuccessors[0][0]): 
                        succ1ACK = ACKNum
                    elif clientID == int(self._immediateSuccessors[1][0]):
                        succ2ACK = ACKNum
                    print("A ping response message was received from Peer %d."%(clientID))
                if self.identifyMsg(msg) == "PING_REQUEST":
                    clientID = [int(n) for n in msg.split() if n.isdigit()][0]
                    print("A ping request message was received from Peer %d."%(clientID))
                    self.sendPingResponse(clientID, msg) 
                    self.updatePredecessors(clientID)
                succ1MissedACKs = pingSeqNum - succ1ACK
                succ2MissedACKs = pingSeqNum - succ2ACK
            except KeyboardInterrupt:
                self.terminateThread(UPDListen_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPListen_thread)
                self.terminateThread(handleUserInput_thread)
                self._TCPServerSock.close()
                self._UDPSock.close()
                self._fileReceiverSock.close()
                os._exit(0)

    # determines whether the message is a peer request message, peer response message, a file request/file response message or if the message contains the data of the file transfer
    
    def identifyMsg(self, msg):
        dec = codecs.getincrementaldecoder('utf8')()
        identifier = ""
        identifier += dec.decode(msg[1:10])
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
        seqNum = [int(n) for n in msg.split() if n.isdigit()][1]
        pingResponse = "*PING_RESPONSE " + "FROM ID: " + str(self._ID) + " SEQUENCE NUMBER: " + str(seqNum)
        self._UDPSock.sendto(pingResponse.encode(), ('localhost', clientID + 50000))                                    # USING UDP   
    
    
    # sends ping request messages to the two immediate successors of a peer every 7 seconds to check if they are alive. Ping request has a sequence number
    def sendPingRequest(self):
        global pingSeqNum
        pingSeqNum = 0
        while True:
            time.sleep(7)
            message = '*PING_REQUEST FROM SENDER ' + str(self._ID) + " SEQUENCE NUMBER " + str(pingSeqNum)
            try:
                if len(self._immediateSuccessors) == 2:
                    self._UDPSock.sendto(message.encode(), self._immediateSuccessors[0][1])                             # USING UDP
                    self._UDPSock.sendto(message.encode(), self._immediateSuccessors[1][1])
                if len(self._immediateSuccessors) == 1:
                    self._UDPSock.sendto(message.encode(), self._immediateSuccessors[0][1])
                pingSeqNum = pingSeqNum + 1
            except KeyboardInterrupt:
                self.terminateThread(UPDListen_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPListen_thread)
                self.terminateThread(handleUserInput_thread)
                self._TCPServerSock.close()
                self._UDPSock.close()
                self._fileReceiverSock.close()
                os._exit(0)
        
    # updates predecessors. invoked when any peer receives a ping response  
    def updatePredecessors(self, predecessorPort):
        if len(self._immediatePredecessors) == 3:
            self._immediatePredecessors.clear()
        if predecessorPort not in self._immediatePredecessors:
            self._immediatePredecessors.append(predecessorPort)
        self.orderPredecessors() # order predecessors
    
    # orders predecessors with self._immediatePredecessors[0] as the immediate predecessor (closest to the peer) and self._immediatePredecessors[1] as the second predecessor (further away from the peer) 
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

    # handles user input based on whether the user input is a file request or if the user input is to make a peer depart gracefully
    def handleUserInput(self):       
        try:
            while True:
                userInput = input()
                if "request" in userInput:
                    fileID = int(re.findall(r'\d+',userInput)[0])
                    fileLocation = (self.hashFunction(fileID)) 
                    requestingPeer = self._ID
                    self.findFileLocation(fileID, requestingPeer, fileLocation, self._ID)
                elif "quit" in userInput:
                    self.sendPeerChurnMsg()
                    self.terminateThread(UPDListen_thread)
                    self.terminateThread(sendPing_thread)
                    self.terminateThread(TCPListen_thread)
                    self.terminateThread(handleUserInput_thread)
                    os._exit(0) 
        except KeyboardInterrupt:
                self.terminateThread(UPDListen_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPListen_thread)
                self.terminateThread(handleUserInput_thread)
                self._TCPServerSock.close()
                self._UDPSock.close()
                self._fileReceiverSock.close()
                os._exit(0)
                  
    # by By Johan Dahlin (http://stackoverflow.com/a/15274929/1800854) for thread termination
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

    # sends a peer churn message to the peer's two immediate predecessors 
    def sendPeerChurnMsg(self):
        try: 
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            sock1.connect((self._IP, self._immediatePredecessors[1]+50000))
            msg1 = "*DEPARTURE_OF PEER " + str(self._ID) + " ONE UPDATE OF SECOND SUCCESSOR TO " + str(self._immediateSuccessors[0][0])
            sock1.send(msg1.encode())                                                                                       # USING TCP
            sock1.close()
            if len(self._immediateSuccessors) >= 2:
                sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock2.connect((self._IP, self._immediatePredecessors[0]+50000))
                msg2 = "*DEPARTURE_OF PEER " + str(self._ID) + " TWO UPDATES: FIRST SUCCESSOR TO " + str(self._immediateSuccessors[0][0]) + " SECOND SUCCESSOR TO " + str(self._immediateSuccessors[1][0])     
                sock2.send(msg2.encode())                                                                                   # USING TCP
                sock2.close()
        except socket.error:
            pass
    
    # sends a find successor request used when a peer is trying to determine its new second successor when there has been an ungraceful peer departure 
    def sendFindSuccessorMsg(self, successor1):
        try:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.connect((self._IP, int(successor1) + 50000))
            msg = "*FIND_IMMEDIATE SUCCESSOR REQUEST FROM PEER " + str(self._ID) + " WITH FIRST SUCCESSOR " + str(successor1)
            sock1.send(msg.encode())
            sock1.close()
        except socket.error:
            pass
    
    # sends the peer's immediate successor when a findSuccessorMsg has been received
    def sendImmediateSuccessorMsg(self, requesterID, successor1):
        try:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.connect((self._IP, int(requesterID) + 50000))
            msg = "*HAVE_FIRST SUCCESSOR " + str(successor1) + " SECOND SUCCESSOR AS REQUESTED: " + str(self._immediateSuccessors[0][0])
            sock1.send(msg.encode())
            sock1.close()
        except socket.error:
            pass
    
    # determines the peer with the closest location to a requested file
    def findFileLocation(self, fileID, requestingPeer, fileLocation, predecessorID):
        successorLocation = int(self._immediateSuccessors[0][1][1])
        successorID = successorLocation - 50000
        peerID = self._ID
        if self.forwardMessage(fileLocation) == True:
            if int(self._ID) != int(requestingPeer):
                print("\n***File %d is not stored here.***\n***File request message has been forwarded to my successor %d.***\n"%(fileID, successorID), file = sys.stderr)    
            else:
                print("\n***File request message has been sent to my successor %d.***\n"%(successorID), file = sys.stderr)
            self.sendRequestFileMsg(requestingPeer, fileLocation, successorLocation, predecessorID, fileID)
        else: 
            print("\n***File %d is here.***\n***A response message, destined for Peer %d, has been sent.***\n"%(fileID, requestingPeer), file = sys.stderr)
            self.sendFileResponse(requestingPeer, fileID)
            self.sendFile(requestingPeer, fileID)
            

    # determines whether or not we need to forward the file request message to a peer's successor based on a distances list - invoked in the forwardMsg function which contains the main logic used to determine whether or not to forward the message to a peer's successor
    def forwardtoSuccessor(self, distances): 
        if distances[2] <= distances[1] and distances[2] <= distances[1]: # that means we should forward
            return True
        elif distances[0] <= distances[1] and distances[0] <= distances[2]:
            return True
        return False

    
    # main logic used to determine whether a peer needs to forward the file request message or not
    def forwardMessage(self, fileLocation):
        peerID = self._ID
        immediateSuccessor = int(self._immediateSuccessors[0][1][1]) - 50000 
        immediatePredecessor = self._immediatePredecessors[0]
        if fileLocation == self._ID:
            return False
        distances = [abs(immediatePredecessor-fileLocation), abs(peerID - fileLocation), abs(immediateSuccessor-fileLocation)]
        if immediateSuccessor > peerID and immediatePredecessor < peerID: # non-wrap around case
            if self.forwardtoSuccessor(distances) == True:
                return True
        if immediateSuccessor < peerID: # just about to come full-circle
            modifiedDistances = [abs(immediatePredecessor-fileLocation), abs(peerID-fileLocation), abs(immediateSuccessor+255-fileLocation)]
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
        msg = "*FILE_REQUEST FILE ID " + str(fileID) + " REQUESTED BY PEER: " +  str(requestingPeer) + " AT LOCATION " + str(fileLocation) + " MESSAGE FORWARDED FROM PEER: " + str(predecessorID)
        self._TCPClientSock.connect((self._IP, successorLocation))                                  
        self._TCPClientSock.send(msg.encode())                                                          # USING TCP
        self._TCPClientSock.close()
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # threaded function used to continually listen to incoming TCP connections and perform certain actions/invoke certain functions depending on the nature of the message received 
    def TCPListen(self):
        self._TCPServerSock.listen(5)
        while True: 
            try:
                conn, clientAddress = self._TCPServerSock.accept()  
                msg = conn.recv(4096) 
                if self.identifyMsg(msg) == "FILE_REQUEST":
                    locations = [int(s) for s in msg.split() if s.isdigit()] 
                    self.findFileLocation(locations[0], locations[1], locations[2], locations[3])
                if self.identifyMsg(msg) == "FILE_RESPONSE":
                    IDs = [int(s) for s in msg.split() if s.isdigit()]
                    peerID = IDs[0]
                    fileID = IDs[1]
                    print("\n***Received a response message from peer %d, which has the file %d.***\n"%(peerID, fileID))
                    print("\n***We now start receiving the file...***\n")
                    self.receiveFile(fileID)
                if self.identifyMsg(msg) == "GRACEFUL_DEPARTURE":
                    departingPeer = [int(s) for s in msg.split() if s.isdigit()][0]
                    successors = [int(s) for s in msg.split() if s.isdigit()][1:]
                    print("\n***Peer %d will depart the network***\n" %(departingPeer))
                    if "ONE UPDATE" in msg.decode(): 
                        firstSuccessor = int(self._immediateSuccessors[0][0])
                        self._immediateSuccessors.clear()
                        self.initialiseImmediateSuccessors(firstSuccessor, successors[0])
                    else: 
                        self._immediateSuccessors.clear()
                        self.initialiseImmediateSuccessors(successors[0], successors[1])
                    print("\n***My first successor is now Peer %d.***\n***My second successor is now Peer %d.***\n"%(int(self._immediateSuccessors[0][0]), int(self._immediateSuccessors[1][0])))
                if self.identifyMsg(msg) == "FIND_SUCCESSOR":
                    requesterID = [int(s) for s in msg.split() if s.isdigit()][0]
                    successor1 = [int(s) for s in msg.split() if s.isdigit()][1]
                    self.sendImmediateSuccessorMsg(requesterID, successor1)
                if self.identifyMsg(msg) == "HAVE_SUCCESSOR": 
                    successor1 = [int(s) for s in msg.split() if s.isdigit()][0]
                    successor2 = [int(s) for s in msg.split() if s.isdigit()][1]
                    self._immediateSuccessors.clear()
                    self.initialiseImmediateSuccessors(successor1, successor2)
                conn.close()
            except KeyboardInterrupt:
                self.terminateThread(UPDListen_thread)
                self.terminateThread(sendPing_thread)
                self.terminateThread(TCPListen_thread)
                self.terminateThread(handleUserInput_thread)
                self._TCPServerSock.close()
                self._UDPSock.close()
                self._fileReceiverSock.close()
                os._exit(0)  

    # used to send a response over TCP to the requesting peer from the peer who is closest to a file       
    def sendFileResponse(self, requestingPeer, fileID):
        msg = "*FILE_RESPONSE BY PEER: " + str(self._ID) + " FOR FILE ID: " + str(fileID)
        self._TCPClientSock.connect((self._IP, requestingPeer+50000))
        self._TCPClientSock.send(msg.encode())                                                                  # USING TCP TO DIRECTLY SEND A FILE
        self._TCPClientSock.close()                                                                             # RESPONSE MESSAGE TO REQUESTING PEER
        self._TCPClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
                                                                                                       
    # used to create a packet with a payload that consists of bytes from the PDF and a header that consists of the required information (ISN, seqNum, MSS)
    def createPacket(self, data, ISN, seqNum):
        header = "***HEADER_*** ISN: " + str(ISN) + " SEQ_NUM: " + str(seqNum) + " MSS: " + str(self._MSS) + " START"
        msg = header.encode('utf-8') + data 
        return msg

    # function used to create log entries for the sender
    def createLogEntrySender(self, retransmit, drop, time, seqNum, dataLen, ACKNum, send):
        if send == True:
            if drop == True:
                if retransmit == True:
                    logEntry = "RTX/Drop\t" + str("%.2f"%time) + "\t\t" + str(seqNum) + "\t\t" + str(dataLen) + "\t\t" + str(0) + "\n"
                else:
                    logEntry = "Drop \t\t"  + str("%.2f"%time) + "\t\t" + str(seqNum) + "\t\t" + str(dataLen) + "\t\t"  + str(0) +"\n"
            elif drop == False:
                if retransmit == True:
                    logEntry = "RTX \t\t" + str("%.2f"%time) + "\t\t"  + str(seqNum) + "\t\t"  + str(dataLen) + "\t\t"  + str(0) + "\n"   
                else: 
                    logEntry = "Snd \t\t"  + str("%.2f"%time) + "\t\t" + str(seqNum) + "\t\t" + str(dataLen) + "\t\t" + str(0) + "\n"
        else:
            logEntry = "Recv \t\t" + str("%.2f"%time) + "\t\t"  + str(0) + "\t\t"  + str(dataLen) + "\t\t"  + str(ACKNum) + "\n"
        return logEntry
    
    # function used to create log entries for the receiver
    def createLogEntryReceiver(self, receive, time, seqNumber, ACK):
        if receive == True:
            logEntry = "Recv \t\t"  + str("%.2f"%time) + "\t\t"  + str(seqNumber) + "\t\t"  + str(ACK-seqNumber) + "\t\t"  + str(0) + "\n"
        else:
            logEntry = "Snd \t\t"  + str("%.2f"%time) + "\t\t" + str(0) + "\t\t" + str(ACK-seqNumber) + "\t\t"  + str(ACK) + "\n"
        return logEntry
    
    
    # function used to send the file, implementing basic reliability in the form of stop and wait behaviour
    def sendFile(self, requestingPeer, fileID): 
        filename = str(fileID) + str(".pdf")
        f=open(filename,"rb")
        logfilename = "sender_log" + "_" + str(fileID) + "_" + str(requestingPeer) + ".txt"
        logfile = open(logfilename, "w+")
        print("\n***We now start sending the file...***\n")
        data = f.read(self._MSS)
        ISN = 1
        seqNum = ISN
        addr = ('localhost', requestingPeer + 60000)
        retransmit = False
        wait = True
        timeout = 1
        while (data):
            wait = True
            if (random.uniform(0,1) >= self._dropProb): 
                msg = self.createPacket(data, ISN, seqNum)
                self._fileSenderSock.sendto(msg, addr) 
                sendTime = time.time()
                if retransmit == True:
                    logfile.write(self.createLogEntrySender(retransmit, False, sendTime, seqNum, len(data), None, True))
                else:
                    logfile.write(self.createLogEntrySender(retransmit, False, sendTime, seqNum, len(data), None, True))
            else: 
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
                        if "ACK" in response.decode():
                            receivedACK = [int(s) for s in response.split() if s.isdigit()][0]
                            if receivedACK == seqNum+len(data):
                                logfile.write(self.createLogEntrySender(None, None, receivedTime, str(0), len(data), receivedACK, False)) 
                                seqNum = seqNum + len(data)
                                data = f.read(self._MSS)
                                wait = False
                    else: 
                        wait = False
                        retransmit = True
                except KeyboardInterrupt:
                    self.terminateThread(UPDListen_thread)
                    self.terminateThread(sendPing_thread)
                    self.terminateThread(TCPListen_thread)
                    self.terminateThread(handleUserInput_thread)
                    self._TCPServerSock.close()
                    self._UDPSock.close()
                    self._fileReceiverSock.close()
                    os._exit(0)
        self._UDPSock.sendto("*END_TRANSFER".encode(),addr)
        print("\n***The file is sent.***\n")
        f.close()   
        
    
    # function that is invoked when a "START_FILE_TRANSFER" msg is received by the requester. Used to receive the PDF file
    def receiveFile(self, fileID): 
            dec = codecs.getincrementaldecoder('utf8')()
            filename = "received_file" + "_" + str(fileID) + "_" + str(self._ID) + ".pdf"
            f = open(filename, "wb") 
            logfilename = "receiver_log" + "_" + str(fileID) + "_" + str(self._ID) + ".txt"
            logfile = open(logfilename, "w+")
            transferOngoing = True
            while(transferOngoing):
                i = 0
                data, addr = self._fileReceiverSock.recvfrom(4096) 
                receiveTime = time.time()
                if self.identifyMsg(data) == "END_FILE_TRANSFER":
                    print("\n***The file is received.***\n")
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
                    recvString = ""
                    numbers = [int(n) for n in header.split() if n.isdigit()]
                    ISN = numbers[0]
                    seqNumber = numbers[1] 
                    MSS = numbers[2]
                    ACK = len(data) - msgStart + seqNumber 
                    if seqNumber == ISN:
                        seqNumOld = ISN
                    if seqNumOld != seqNumber or seqNumber == 1:
                        logfile.write(self.createLogEntryReceiver(True, receiveTime, seqNumber, ACK))
                    f.write(data[msgStart:msgStart+MSS]) 
                    ACKmsg = "*****ACK_*****: " + str(ACK) + " "
                    self._fileReceiverSock.sendto(ACKmsg.encode(), addr)
                    sendTime = time.time()
                    logfile.write(self.createLogEntryReceiver(False, sendTime, seqNumber, ACK))
                    seqNumOld = seqNumber
           
        
if __name__ == "__main__":
    p1 = Peer(sys.argv[1], sys.argv[4], sys.argv[5])  
    p1.initialiseImmediateSuccessors(sys.argv[2],sys.argv[3])
    p1.bindSock()
    UPDListen_thread = threading.Thread(target = p1.UPDListen, args = ())
    sendPing_thread = threading.Thread(target = p1.sendPingRequest, args = ())
    TCPListen_thread = threading.Thread(target = p1.TCPListen, args = ())
    handleUserInput_thread = threading.Thread(target = p1.handleUserInput, args = ())
    sendPing_thread.daemon = True
    UPDListen_thread.daemon = True
    TCPListen_thread.daemon = True
    handleUserInput_thread.daemon = True
    sendPing_thread.start()
    UPDListen_thread.start()
    TCPListen_thread.start()
    handleUserInput_thread.start()
    sendPing_thread.join()
    UPDListen_thread.join()
    TCPListen_thread.join()
    handleUserInput_thread.join()


    


