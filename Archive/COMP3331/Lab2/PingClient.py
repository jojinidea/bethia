# Bethia Sun
# z5165555
# Ping Client task (Exercise 5 of Lab2)

import time
from socket import *
import sys

portNum = int(sys.argv[1]) #extract portNum from command line arguments
RTTlist = []
index = 0
pings = 0 

# send ping 10 times
while pings < 10:

    # create UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1) # sets timeout value of 1 second
    message = 'PING {} {} \r\n'.format(pings, time.time()) 
    address = ('localhost', portNum)
    
    # send ping
    start = time.time()
    clientSocket.sendto(message,address)
    
    try:
        data, server = clientSocket.recvfrom(2048) # recv return value is pair (string,address) - where string is a string representing data received and address is the address of the socket sending the data
        end = time.time()
        elapsed = end - start
        RTTlist.insert(index, elapsed)
        index += 1
        print ("Ping to {} port {}, seq = {}, rtt = {:.3f}ms".format(address[0], address[1], pings,elapsed*100))

    except timeout:
        print ("Ping to {} port {}, seq = {}, rtt = REQUEST TIMED OUT".format(address[0], address[1], pings)) 
        
    finally: 
        pings = pings + 1
        
# report min, max and average RTTs
print ("Minimum RTT is {:.3f}ms, maximum RTT is {:.3f}ms, average of all successful packet transmissions is {:.3f}ms".format(min(RTTlist)*100, max(RTTlist)*100, (sum(RTTlist)/len(RTTlist))*100))
