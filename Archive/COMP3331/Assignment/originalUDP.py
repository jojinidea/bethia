from socket import *
import sys
import time

s = socket(AF_INET, SOCK_DGRAM)
port = 9999
buf = 1024
addr = ('localhost', port)
file_name = sys.argv[1]
MSS = sys.argv[2]
s.sendto(file_name, addr)
f=open(file_name, "rb")
data = f.read(MSS)

# set timer after we send the message
# if ack received continue
# otherwise, if ACK not received, we need to retransmit the packet
# let's put the sequence number in the string and the ACK number
# we will remove these numbers from the length of the message (they are in the header)

# generate random num to set as sequence number
# sequence number is always equal to number of bytes sent 
# ack number is seq no + len(data) - next expected byte
# ACK NUM = 


while(data):
    data = str(sequenceNum) + data
    sequenceNum = sequenceNum + len(data)
    s.sendto(data, addr)
    start = time.time()
        print("Sending...")
    if timeout:
        # retransmit 
    else: # advance buffer
        data = f.read(buf)
s.close()
f.close()
