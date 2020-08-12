from socket import *
import select
import sys
import codecs
dec = codecs.getincrementaldecoder('utf8')()
import random
import time

# ADD THE TIME IN
# MERGE INTO CODE 

s = socket(AF_INET,SOCK_DGRAM)
port = 9999
addr = ('localhost', port)

file_name=sys.argv[1]
MSS = int(sys.argv[2])
dropProb = float(sys.argv[3])
s.sendto(file_name.encode(),addr)
s.sendto("TRANSFER START".encode(),addr)
print("We now start sending the file...")
f=open(file_name,"rb")
logfile = open("sender_log.txt", "w+")
seqNum = 1
data = f.read(MSS)
timeout = 1 # in seconds
retransmit = False
wait = True

def createPacket(data, seqNum):
    header = "HEADER SEQ_NUM: " + str(seqNum) + " START"
    print(header)
    msg = header.encode('utf-8') + data # append header to msg
    return msg

def createLogEntrySender(retransmit, drop, time, seqNum, dataLen, ACKNum, send):
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
        logEntry = "Type of message: Recv \t" + "Time: " + str("%.2f"%time) + "\t" + "Seq number: " + str(0) + "\t" + "Data size: " + str(dataLen) + "\t" + "ACK num: " + str(receivedACK[0]) + "\n"
    return logEntry


while (data):
    if (random.uniform(0,1) > dropProb): # we have not dropped the packet, so send it and write the corresponding logfile entry
        msg = createPacket(data, seqNum)
        s.sendto(msg, addr) 
        sendTime = time.time()
        if retransmit == True:
            logfile.write(createLogEntrySender(retransmit, False, sendTime, seqNum, len(data), None, True))
        else:
            logfile.write(createLogEntrySender(retransmit, False, sendTime, seqNum, len(data), None, True))
    else: # we have dropped the packet, write corresponding logfile entry
        dropTime = time.time()
        if retransmit == True:
            logfile.write(createLogEntrySender(retransmit, True, dropTime, seqNum, len(data), None, True))
        else:
            logfile.write(createLogEntrySender(retransmit, True, dropTime, seqNum, len(data), None, True))
    retransmit = False
    wait = True
    while wait == True:
            ready = select.select([s],[],[],timeout)
            try: 
                if ready[0]:
                    receivedTime = time.time()
                    response, clientAddress= s.recvfrom(4096) 
                    if "ACK" in response.decode():
                        receivedACK = [int(s) for s in response.split() if s.isdigit()]
                        #print(receivedACK)
                        #print("received ACK num is %d, expected ACKNum is %d."%(receivedACK[0], seqNum+len(data)))
                        if receivedACK[0] == seqNum+len(data):
                            # write recv time, sequence number = 0, size of data, ACK = receivedACK
                            logfile.write(createLogEntrySender(None, None, receivedTime, str(0), len(data), receivedACK[0], False))
                            #print("Advancing buffer")
                            seqNum = seqNum + len(data)
                            data = f.read(MSS)
                            wait = False
                        else:
                            print("Incorrect ACK #")
                    else:
                        print("No ACK received yet")
                else: # no ACK received before timeout
                    retransmitTime = time.time()
                    print("Timeout, starting retransmsision")
                    wait = False
                    retransmit = True
            except KeyboardInterrupt:
                sys.exit(1)

print("The file is sent...")
s.sendto("FIN_FILE START".encode(), addr)

        
s.close()
f.close()

