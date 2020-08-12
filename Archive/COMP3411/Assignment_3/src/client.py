import socket
import sys
import errno
import re
import random
import numpy as np
from game import *
from agent import *

class TTTClient(object): 
    # deals with communication with the tic tac toe server
    
    def __init__(self, portNum):
    # initialises TTTclient by creating socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._connected = False
        self._portNum = portNum
        self._IP = 'localhost'
    
    # connects to server
    def connect(self):
        address = (self._IP, self._portNum)
        try: 
            self._socket.connect(address) # connects to address
            self._connected = True
        except socket.error as e: 
            print("Error connecting to server")
        except KeyboardInterrupt:
            print("Keyboard interrupt, exiting program")
            sys.exit(1)
 
    # receives a message from the server
    def receive(self):
        try:
            message = self._socket.recv(2048)
            return (message.decode("utf-8"))
        except socket.error as e:
            print("Error receiving data")
            sys.exit(1)
    
    # closes server
    def close(self): 
        self._socket.close()         

# deals with game logic on client side
            
class TTTClientGame(TTTClient):

    def __init__(self, portNum):
        super(TTTClientGame, self).__init__(portNum)
    
    def parse_string(self, string):
        if "(" in string:
            command, args = string.split("(")
            args = args.split(")")[0]
            args = args.split(",")
        else:
            command, args = string, []
        return [command, args] # returns a list with the command and the arguments (if applicable)


