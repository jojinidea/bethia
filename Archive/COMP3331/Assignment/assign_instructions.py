# COMP3331 Assignment
# 5 input arguments - first three input arguments are integers in range [0,255], fourth input is an integer value, final input is a value in range [0,1]
# indicate what version of python used in report
# NEED TO WRITE A REPORT

# Step 1 Initialisation:
# if we have 8 peers, 8 xterms will be open to initialise these peers python cdht.py 1 3 4 400 0.1 
# first argument is identity of peer to be intiialised, second and third arguments - i.e. 3 and 4 are identities of successive peers, fourth argument is max segment size used to determine size of data to be transferred. last argument is drop probability 
# can assume P2P network at most 10 peers
# min # peers is 4
# identity always in range [0,255]
# set up script correctly describes circular DHT

# Step 2 Ping Successors
# after initialisation each peer will ping two successors to see whether they are alive
# should define two types of messages - ping request and ping response
# use UDP protocol 
# can assume that peer with identity i will listen to UDP port 50000 + i for ping messages - e.g. peers 4 and 12 will listen to UDP ports 50004 and 50012 
# each peer outputs line to terminal when ping request message received from any of its two predecessors - "A ping request message was received from Peer x" or "A ping response message was received from Peer x"
# messages must differentiate between ping response and ping request messages
# we can decide how often to send ping requests

# Step 3 Requesting a file
# to request a file with name X from peer Y, requester will type request X to xterm of peer Y
# filenames are four digit numbers (NO letters) - e.g. 0000
# need to apply hash function to this filename - each filename is an int in range [0, 9999]. to compute hash of file, we compute remainder of filename integer when divided by 256 - e.g. 2012/256 = 220 (so hash of file is 220). Values are in range of [0, 255]
# if the file's hash value is n, the file will be stored in the peer that is the closest successor of n - if hash values of 3 different files are 6, 10, 210, they will be stored in peers 8, 10, 1
# request and response messages: if a peer wants to request a file, the requesting peer will send a file request message to successor (this will be passed around P2P network until it reaches peer with the file - the responding peer). The responding peer will send a response message directly to requesting peer. These messages (request and response) must be sent over TCP (TCP port 50000 + i for these messages)
# transferring files - responding peer must transfer file to requesting peer over UDP connection (file must be sent directly to requesting peer). UDP not reliable so need to implement reliability by using stop and wait behaviour - if ACK received, sender sends next part of data, otherwise if timeout happens, sender retransmits. Responding peer forms packet with MSS bytes of data - adds sequence number, ACK number and MSS and encapsulate all as a packet - this will be transmitted to requesting peer. Responding peer will start timer for packet which is essentially needed for timeout operation. Once requesting peer received this data packet, it will generate ACK and send pack to responding peer
# timeout interval is set to 1 second
# peers must maintain log file named 'responding_log.txt' and 'requesting_log.txt'
# record information about each segment they send and receive - in format <event> <time> <sequence-num> <# bytes of data> <ACK number>  where event = snd/rcv/drop/RTX and ,time. is time since start of program
# drop_rate value as input which is probability in which packets dropped
# before delivering packet to socket to be sent to requesting peer, responding peer creates random number (between 0-1) and checks if random number smaller than drop probability - if yes, responding peer will not send the packet. Timer set by responding peer will eventually reach timeout, which triggers re-transmission. In log file, print log corresponding to drop packet when packet is dropped



