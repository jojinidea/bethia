import csv

def read(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    #creates a reader, passes a filehandle to it
    
    for row in reader:
        print(reader)
        
        
    f.close()
    

def write(filename, payload): 
    f = open(filename, 'w')
    writer = csv.writer(f)
    writer.writerow(payload)
    f.close()
    
    pass
    
    write('basic_csv.csv', ['Hello there'])
