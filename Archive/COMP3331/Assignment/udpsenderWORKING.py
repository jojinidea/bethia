from socket import *
import select
import sys
import codecs
dec = codecs.getincrementaldecoder('utf8')()
import random

# IMPLEMENT TIME FOR THE LOGS & ALSO IMPLEMENT DATA SIZE (not just MSS)  

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

while (data):
    # create a packet
    if (random.uniform(0,1) > dropProb):
        msg = createPacket(data, seqNum)
        s.sendto(msg, addr) # send packet
        if retransmit == True:
            logEntry = "Type of message: RTX \t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(len(data)) + "\t" + "ACK num: " + str(0) + "\n"
            logfile.write(logEntry)
        else:
            logEntry = "Type of message: snd \t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(len(data)) + "\t" + "ACK num: " + str(0) + "\n"
            logfile.write(logEntry)
    else:
        # write to log file, 
        if retransmit == True:
            logEntry = "Type of message: RTX/Drop \t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(len(data)) + "\t" + "ACK num: " + str(0) + "\n"
            logfile.write(logEntry)
        else:
            logEntry = "Type of message: Drop \t" + "Seq number: " + str(seqNum) + "\t" + "Data size: " + str(len(data)) + "\t" + "ACK num: " + str(0) +"\n"
            logfile.write(logEntry)
    retransmit = False
    wait = True
    while wait == True:
            ready = select.select([s],[],[],timeout)
            try: 
                if ready[0]:
                    response, clientAddress= s.recvfrom(4096) 
                    # check value of ACK against seq number calculated
                    print("msg is", response)
                    if "ACK" in response.decode():
                        receivedACK = [int(s) for s in response.split() if s.isdigit()]
                        print(receivedACK)
                        print("received ACK num is %d, expected ACKNum is %d."%(receivedACK[0], seqNum+len(data)))
                        if receivedACK[0] == seqNum+len(data):
                            # write recv time, sequence number = 0, size of data, ACK = receivedACK
                            logEntry = "Type of message: Recv \t" + "Seq number: " + str(0) + "\t" + "Data size: " + str(len(data)) + "\t" + "ACK num: " + str(receivedACK[0]) + "\n"
                            logfile.write(logEntry)
                            print("Advancing buffer")
                            seqNum = seqNum + len(data)
                            data = f.read(MSS)
                            wait = False
                        else:
                            print("Incorrect ACK #")
                    else:
                        print("No ACK received yet")
                else: # no ACK received before timeout
                    print("Timeout, starting retransmsision")
                    print("Retransmitting")
                    wait = False
                    retransmit = True
            except KeyboardInterrupt:
                sys.exit(1)

print("The file is sent...")
s.sendto("FIN_FILE START".encode(), addr)

        
s.close()
f.close()

