import pickle

def readp(filename):
    f = open(filename, 'rb') 
    return pickle.load(filename)
    #reads it in byte-stream
    
    
def writepickle(filename, payload):
    f = open(filename, 'wb')
    
    pickle.dump(payload, f) 
    f.close()

writepickle('output.pkl', ['A', 2,3,4])
print(readp('output.txt'))

#converts objects into bytestream, and then we can load the bytestream through a filehandle and convert it back to what it was before
