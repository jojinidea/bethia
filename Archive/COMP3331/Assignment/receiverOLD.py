from socket import *
import select
import sys
import codecs
dec = codecs.getincrementaldecoder('utf8')()
import random

s = socket(AF_INET,SOCK_DGRAM)
port = 9999
addr = ('localhost', port)

file_name=sys.argv[1]
MSS = int(sys.argv[2])
dropProb = float(sys.argv[3])
s.sendto(file_name.encode(),addr)
f=open(file_name,"rb")
data = f.read(MSS)
seqNum = 1
timeout = 1 # in seconds

while (data):   
    wait = True
    ACKNum = seqNum + len(data)
    msg = data
    header = "HEADER ACK_NUM: " + str(ACKNum) + " SEQ_NUM: " + str(seqNum) + " START"
    print(header)
    msg = header.encode('utf-8') + msg # append header to msg
    print("Length of message is %d" %(len(msg)))
    if (random.uniform(0,1) > dropProb):
        s.sendto(msg, addr) # send packet
        seqNum = seqNum + len(data) # new seq num is old seq num + length of data sent 
        print("Sent packet")
    
    while wait == True:
            ready = select.select([s],[],[],timeout)
            try: 
                if ready[0]:
                    response, clientAddress= s.recvfrom(4096) 
                    # check value of ACK against seq number calculated
                    print("msg is", response)
                    if "ACK" in response.decode():
                        receivedACK = [int(s) for s in msg.split() if s.isdigit()][0]
                        print("received ACK num is %d, expected seqNum is %d."%(receivedACK, seqNum))
                        if receivedACK == seqNum:
                            print("Advancing buffer")
                            data = f.read(MSS)
                            wait = False
                        else:
                            print("Incorrect ACK #")
                    else:
                        print("No ACK received yet")
                else: # no ACK received before timeout
                    print("Timeout, starting retransmsision")
                    print("Retransmitting")
                    s.sendto(msg, addr)
                    data = f.read(MSS)
                    print("SENT MSG")
                    wait = False
            except KeyboardInterrupt:
                sys.exit(1)


        
s.close()
f.close()

