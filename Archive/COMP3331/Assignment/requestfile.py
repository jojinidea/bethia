# aims for today:
    # requesting peer initialises and sends file request to successor (initialise a packet and send to successor once 'request x' typed to terminal) SENT OVER TCP
    # forwarding request to correct node with the file (intermediate peers must show proper message they received & forward the request) 
    # send response from node with the file to the requester using TCP (requester has to print it sends response to requesting peer)

# findFileLocation() - determines location of the file
# requestFile() - send messages to successors, passing them around P2P network until we reach the peer that has the file using TCP
# sendResponse() - peer with the file sends response directly to peer who requested file using TCP





# using P2P network you have created to request file
# to request a file with filename X from Y, requester will type request X into xterm of peer Y

# filename - all filenames are four digits numbers (e.g. 0000, 0159, 1890 etc)
# hash function - all peers use same hash function (remainder of the filename integer when divided by 256) - e.g. 2012/256 has remainder 220 (so hash is 220)
# file location - depends on hash of a file as well as # peers in network
    # for a file whose hash is n, file will be stored in a peer that is the closest successor of n
    # if hash values of 3 different files are 6, 10, 210, they will be stored in 8, 10 and 1 (with DHT 1-3-4-5-8-10-12-15)
# request and response messages - if peer wants to request for a file, requesting peer sends a file request message to successor. This message will be passed around P2P network until it reaches the peer that has the file (responding peer)
    # responding peer sends a response message directly to requesting peer over TCP
# transfer the file
    # responding peer transfers file directly to requesting peer over UDP connection DIRECTLY to requesting peer (unlike with ping packets)
    # need to make connection reliable by implementing simple stop and wait
        # sender sends data packet to receiver and waits until ACK received/timeout
        # if ACK received, sender sends next part of data
        # if timeout occurs, sender retransmits data
        # responding peer forms packet with MSS bytes of data
        # adds sequence number, ACK number and MSS and encapsulates all as a packet
        # packet then transmitted to requesting peer
        # responding peer needs to start a timer for timeout operation
        # once requesting peer received the packet, generates a corresponding acknowledgement and sends back to the responding peer
        # on receipt of this packet, responding peer transfers next MSS bytes of data
        # if packet lost, requesting peer does not send ACK and timeout happens
        # responding peer maintains timer for each data packet it sends
        # timeout interval set to 1 in this assignment
        # if responding peer does not receive ACK for sent packet within timeout interval - packet loss, so we need to retransmit
        # responding and requesting peers maintain a log file named responding_log.txt and requesting_log.txt where they record the info about each segment they send and receive with some format (refer to assignment)
        # drop-rate: before sending packet to requesting peer, responding peer creates a random number (between 0-1) and checks if random number smaller than drop prob. If yes, responding peer will not send the packet. The timer set by the responding peer will eventually reach the timeout interval which triggers packet re-transmission
        # print log corresponding to drop packet 

