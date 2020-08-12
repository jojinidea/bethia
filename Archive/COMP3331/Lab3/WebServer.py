# Bethia Sun
# z5165555
# Ping Server task (Exercise 4 of Lab3)

import time
from socket import *
import sys

portNum = int(sys.argv[1]) #extract portNum from command line arguments
sock = socket(AF_INET, SOCK_STREAM)
server_address = ('localhost', portNum)
sock.bind(server_address) 
sock.listen(1)

while True: 
    connection, client_address = sock.accept()   
    req = connection.recv(1024).decode('utf-8') 
    string_list = req.split(' ') 
    requested_file = string_list[1]
    filename = requested_file[1:]
    # print('Requested file is {}'.format(filename))
    
    try: 
        file = open(filename, 'rb')
        response = file.read()
        file.close()
        
        header = 'HTTP/1.1 200 OK\n'
        
        if(filename.endswith(".png")):
            filetype = 'image/png'
        else:
            filetype = 'text/html'
        
        header += 'Content-Type:' +str(filetype)+'\n\n'
        
    except Exception as e: 
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html> <body> <center> <h1> Error 404: File not found </h1> </center> </body> </html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()



