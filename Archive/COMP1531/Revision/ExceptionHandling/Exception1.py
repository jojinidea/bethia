try: 
    file = open("testfile", "w")
    file.write("some writing to a test file")
except IOError:
    print("Error occured in writing to the file")
    #no exceptions are handled, so execution jumps from line 3 to line 7
else:
    print("Successfully written to the file")
finally: #always executed!!
    print("All done")
    
