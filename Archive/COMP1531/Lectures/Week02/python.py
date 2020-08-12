#to define an empty list, variable = []
#to define a list with items in it, variable = [1,2,3,4]

li = ["Hello",2,3,4,5,6]
print(li)

#lists are mutable (but not strings), we can change indexes of the list. Lists also have indexes

#lists can also store any type of data-type

li[0] = 9
print(li)


#list append allows us to append something to the end of the list

li.append("appended this") #b is appended to the end of the list
print(li)


#list insert - takes in the index of the list and something you want to replace the list with
li.insert(0,"Insert") #this inserts "insert" at the zeroth index
print(li)

#list pop - we can provide an index to pop as well (or no index)
a = li.pop() #pops the last number off the list (also returns this element)
print(a)

#iterating through a list - for element in container: do soething
for element in li: 
    print(element) 
    
#li2 = [[1,2,3], [1], 2, [[1,2,3],3], 4] - index 0 is [1,2,3]

#tuples - basically lists but immutable. defined by tup = ()

tup = (1,2)
# tup[0] = 2 - will not work

#python sets
s = {1,2,3,3,3,4,4}
print(s) 
#sets do not contain duplicate values inside, so all the duplicate values are removed

#set and list constructors
li = [1,2,2,2]
set(li) #gets rid of duplicate values
print(set(li))
list(set(li)) #converts the list without duplicate values into a list

#union, intersection, difference
# a | b union
# a - b difference
# a & b intersection

# Dictionary - declared by variable = {}
# keys in the python dictionary MUST be immutable objects
dictionary = {}
dictionary['A'] = 1
dictionary[5] = 2
print(dictionary['A']) #prints associated value with A
# A is the key, 1 is the value I'm storing against A

# key -> hashing function -> index 
# key is the argument to the hashing function, the hashing function will return an int

# 'A' -> hashing function -> 6
# 5 -> hashing function -> 1
# will find the index 6, and put the value at that index
# will store the number associated with 5 at the index 1
# [None, 2, None, None, None, None, 1]

# ERROR: Keys MUST be immutable objects
# li = [1,2,3]
# dictionary[li] = 'A'
# li.append(1)
# dictionary[li] #hashing function will now give us a different index value as li is no longer the same list

# returns value at that position - that value is associated with that key

# Iterating through keys
for key in dictionary:
    print(key)

# Iterating through values
for val in dictionary.values():
    print(val)

# Iterating through both - returns the key and the value pair
for k, v in dictionary.items(): 
    print(k, "->", v)

# ORDER IS NOT MAINTAINED

# Functions - def is used to define a function, arguments put in
# def function(arg1, arg2):
#do something, no return value needed

def sumn(a,b):
    return a + b
    
li = [1,2]
print(sumn(*li)) 
# *li will unpack values in a list li, associate 1 with a and 2 with b

# default args - put non-default arguments at the start, default arguments at the start
def increment(num, incr=1):
    return num + incr

print(increment(3,incr=2)) # prints 5
print(increment(3)) #prints 4 (adds 1 with 3, as default argument is 1)


#modules in python
#similar to a header in C
#imagine that name_of_the_file contains the sumn function above

#import name_of_the_file
#some_module.sumn(1,2)
#we can also refer to values in the modules e.g. print(some_module.VAR)

#we can access things in the module
#when you are running a normal python file, it assumes that file is the main

#opening files
#filename
#f = open(filename, 'mode') - e.g. 'w', 'r', 'a'
filename = 'input.txt'
f = open(filename, 'r')
#the above will return a filehandle for that filename
print(f.read()) #reads whole file
print(f.readlines()) #reads line by line - if we print this it prints each line as a string member inside a list
f.close() #closes the file
f = open(filename, 'w') #opens file for writing
f.write('Lecture 18s2 COMP1531') #will OVERwrite everything in the file, 'a' flag is appending the new line to the file


#csv files
#basically like spreadsheets - two columns





    


    



