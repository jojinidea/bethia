# import all the files

import socket
import sys
import errno

# we will need to get the moves from the agent and write it to the output file, as well as passing the information received by the client to the update board function


class Client(object): 
    # deals with communication with the tic tac toe server
    
    def __init__(self, portNum):
        # initialises client by creating socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False
        self._portNum = portNum
        self._IP = 'localhost'
    
    def connect(self):
        # connects to server
        address = (self._IP, self._portNum)
        try: 
            print("Attempting to connect to the server...")  
            self._socket.connect(address) # connects to address
            self._connected = True
        except socket.error as e: 
            print("Error connecting to server")
        except KeyboardInterrupt:
            print("Keyboard interrupt, exiting program")
            sys.exit(1)
 
    def receive(self):
        # receives a message from the server
        print("Waiting to receive message from server")
        try:
            message = self._socket.recv(2048)
            sys.stdout.write(message.decode("utf-8"))
        except socket.error as e:
            print("Error receiving data")
            sys.exit(1)
         
            
    def main_loop(self):
        while True:
            self.receive()
    
def main():
    client = Client(portNum)
    client.connect()
    client.main_loop()
    

if __name__ == "__main__":
    portNum = int(sys.argv[1])
    main()
      
# server simply reads output on terminal I think... 
