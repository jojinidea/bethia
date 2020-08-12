# ----- receiver.py -----

#!/usr/bin/env python

from socket import *
import sys
import select
import codecs
dec = codecs.getincrementaldecoder('utf8')()
buff = sys.argv[1]


host="0.0.0.0"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=2048

data,addr = s.recvfrom(buf)
print "Received File:",data.strip()
f = open(data.strip(),'wb') # filename
logfile = open("receiver_log.txt", "w+")
s.settimeout(30)

try:
    while(data):
        data,addr = s.recvfrom(buf)
        # get time that we received message, write sequence number, ACK number = 0
        recvString = ""
        i = 0
        #print("Length of data is %d"%(len(data)))
        while " START" not in recvString:  
            recvString += dec.decode(data[0:i])
            i = i+1
        header = ""
        header += dec.decode(data[0:i-1])
        print(header)
        if "TRANSFER" in header:
            print("We now start receiving the file...")
        elif "FIN_FILE" in header:
            print("The file is received...")
            break
        else:
            headerLength = len(header)
            msgStart = headerLength
            print("msg start is", msgStart)
            recvString = ""
            f.write(data[msgStart:msgStart+int(buff)])
            numbers = [int(n) for n in data.split() if n.isdigit()]
            seqNumber = numbers[0] 
            ACK = len(data) - msgStart + seqNumber # ACK is the length of the data (not including header) + sequence num
            logEntry = "Type of message: recv \t" + "Seq number: " + str(seqNumber) + "\t" + "Data size: " + str(ACK-seqNumber) + "\t" + "ACK num: " + str(0) + "\n"
            logfile.write(logEntry)
            #print("Seq number is", seqNumber)
            print("ACK = len(data) %d - msgStart %d + seqNum %d"%(len(data), msgStart, seqNumber))
            ACKmsg = "ACK: " + str(ACK) + " "
            print("Sending ACK", ACKmsg)
            # get time
            # send, time, sequence number = 0, len(payload) = len(data) - msgStart, MSS, ACK number 
            s.sendto(ACKmsg.encode(), addr)
            logEntry = "Type of message: Send \t" + "Seq number: " + str(0) + "\t" + "Data size: " + str(ACK-seqNumber) + "\t" + "ACK num: " + str(ACK) + "\n"
            logfile.write(logEntry)
            #s.sendto("garbage".encode(), addr)
            print("ACK sent", ACKmsg)

except timeout:
    f.close()
    s.close()
    print "File Downloaded"
