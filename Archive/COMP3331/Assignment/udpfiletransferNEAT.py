from socket import *
import select
import sys
import codecs
import random
dec = codecs.getincrementaldecoder('utf8')()

s = socket(AF_INET,SOCK_DGRAM)
s.setblocking(0)
port = 9999
addr = ('localhost', port)

file_name=sys.argv[1]
MSS = int(sys.argv[2])
s.sendto(file_name.encode(),addr)
f=open(file_name,"rb")
data = f.read(MSS)
ISN = random.randrange(1,1000)
seqNum = ISN
timeout = 1 # in seconds

def encapsulateMsg(data, ACKNum, seqNum):
    header = " START_HEADER ACK_NUM: " + str(ACKNum) + " SEQ_NUM: " + str(seqNum) + " "
    headerLength = (len(header)) # compute header Length 
    msg = str(headerLength).encode('utf-8') + header.encode('utf-8') + msg # append header to msg
    return msg

while (data):   
    ACKNum = seqNum + len(data) 
    msg = data
    msg = encapsulateMsg(data, ACKNum, seqNum)
    if(s.sendto(msg,addr)):
        print("sending ...")
        seqNum = seqNum + len(data) # new sequence number is old sequence number plus length of the data that has been sent
        ready = select.select([s],[],[],timeout)
        try:
            if ready[0]:
                msg, clientAddress= s.recvfrom(4096) 
                ACKnum = [int(s) for s in msg.split() if s.isdigit()]
                if ACKnum[0] == seqNum: # check value of ACK against seq Num of next packet
                    data = f.read(MSS) # advance buffer
            else: # no ACK received before timeout
                print("Timeout, starting retransmsision")
                print("Retransmitting")
                s.sendto(msg, addr)
        except KeyboardInterrupt:
            sys.exit(1)
        
s.close()
f.close()


