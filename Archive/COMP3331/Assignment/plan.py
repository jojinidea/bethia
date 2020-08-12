











# have a function called ping - pass in successors, ping both

# plan
# one main class - peer
    # attributes from command line: peerID, 2 immediate successors, MSS, drop prob
    # other attributes: socket
    # immediate successors a tuple with the ID as first element, address as second element
    # methods:
    # server method - always running in background waiting for incoming connections
    # client method - send pings to neighbour

# goal - when we open the terminal and run the program, let's be a server (listen for connections, receive messages) and also a client (send messages to 2 immediate successors)
  
# create a thread
# need two sockets - separate socket/thread for listening and sending

  
# initialise the DHT 

# peer ID, 2 immediate successors, MSS, drop prob
# when we open the terminal and run the program, let's be a server and send messages to the two successive neighbours
# have a server method that is always run
# have a client method
# send pings as a client to a server
# receive pings at the same time


