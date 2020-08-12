from socket import *
import select
import sys
import codecs
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
seqNum = 1
timeout = 1 # in seconds

while (data):   
    ACKNum = seqNum + len(data) 
    msg = data
    header = "HEADER ACK_NUM: " + str(ACKNum) + " SEQ_NUM: " + str(seqNum) + " START"
    msg = header.encode('utf-8') + msg # append header to msg
    #bytes = len(str(headerLength)) # compute number of bytes needed to encode header length 
    print(msg)
    recvString = ""
    #msgStart = headerLength + bytes
    #print("msg start is %d"%(msgStart))
    #recvString +=dec.decode(msg[0:headerLength+bytes])
    #print("recv string is", recvString)
    if(s.sendto(msg,addr)):
        print("sending ...")
        seqNum = seqNum + len(data) # new sequence number is old sequence number plus length of the data that has been sent
        try:
            s.settimeout(2)
            msg, clientAddress= s.recvfrom(4096) 
            ACKnum = [int(s) for s in msg.split() if s.isdigit()]
            print("ACK num is %d, expected seqNum is %d."%(ACKnum[0], seqNum))
            if ACKnum[0] == seqNum:
                    # advance buffer
                data = f.read(MSS)
        except socket.timeout:
            print("Timeout, starting retransmsision")
            print("Retransmitting")
            s.sendto(msg, addr)
        
s.close()
f.close()

