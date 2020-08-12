#f = open('testfile.txt') #if this file does not exist, we get an error on the terminal (helpful to us as developers but not useful for the users)

try:
    f = open('testfile.txt') #try to do something, throws an exception, so then we go to the except block, prints out the line there
except FileNotFoundError: 
# we can change this to a FileNotFoundError
    print('Sorry. This file does not exist')
except Exception as e: #Exception: general exception will catch multiple errors, we want to make this more specific
    print(e) #prints out exception that we hit
else: #runs code if try-except clause does not raise an exception
    print(f.read()) 
    f.close() 
    #try does not run an exception, so this else block executes
finally: #finally clause runs no matter what happens (regardless of whether code successful or if we run into except blocks) 
    #useful for releasing memory
    print("Executing Finally...")
    
    
