# import all the files

import socket
import sys
import errno

class TTTClient(object): 
    # deals with communication with the tic tac toe server
    
    def __init__(self, portNum):
        # initialises TTTclient by creating socket
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
        #print("Waiting to receive message from server")
        try:
            message = self._socket.recv(2048)
            #print("Message received is:\n") # for debugging
            #sys.stdout.write(message.decode("utf-8"))
            return (message.decode("utf-8"))
        except socket.error as e:
            print("Error receiving data")
            sys.exit(1)
         
            

class TTTClientGame(TTTClient):

# deals with game logic on client side

    def __init__(self, portNum):
        super(TTTClientGame, self).__init__(portNum)
    
    
    def parse_string(self, arg, msg)
        # returns required piece of information from string used to get information about the game state
    
    def start_game(self):
        while True:
            serverMessage = self.receive()
            msgList = serverMessage.split('\n') # used to split multiple messages received as part of the continuous byte stream
            for i in range(0, len(msgList)):
                msg = msgList[i]
                if "init." in serverMessage:
                    sys.stdout.write("Received init.")
                if "start" in serverMessage:
                    sys.stdout.write("initialise player")
                    # initialise player with letter
                if "second_move" in serverMessage:
                    sys.stdout.write("Received second move")
                    # update board, first number is board number, second number is previous move
                if "third_move" in serverMessage:
                    sys.stdout.write("Received third move")
                    # update board
                if "next_move" in serverMessage:
                    sys.stdout.write("Received next move")
                    # invoke client's next move
                if "last_move" in serverMessage:
                    print("Received last move")
                if serverMessage.find("end\n"):
                    print("Cleaning up")
                    # invoke cleanup
                print("End of while loop")
                # agent.c also gets the cause of wins and losses
            
def main():
    portNum = int(sys.argv[1])
    # initialise client object
    client = TTTClientGame(portNum)
    client.connect()
    try:
        client.start_game()
    except:
        print("Game finished unexpectedly!")


if __name__ == "__main__":
    main()
      
