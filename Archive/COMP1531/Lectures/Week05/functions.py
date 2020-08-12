def hello_world(name):
    return "hello world" + name
    
    
my_function = hello_world
print(my_function('sally'))
#the same as hello_world('jack')
#assigns function to variable

def nested_hello_world(name):
    def greet():
        return "Hello world " 
    return greet() + name # makes call to internal function greet - returns "Hello world" and adds name
my_function = nested_hello_world #assign function to the variable
print(my_function('samuel'))

#functions returning other functions

def greet(name,lang):
    if lang == 'French'
        return "Bonjour"
    else:
        return "Hello World" 
        
def another_hello_world(some_function):
    my_name = "Jack"
    my_lang = "French"
    return greet(my_name,my_lang)
    
print(another_hello_world(greet)) #greet is the "some_function" that is invoked by another_hello_world 

#functions returning other functions
def yet_another_hello_world():
    def greeting(name):
        return "Hello world" + name
    return greeting #greeting() - invoking the function - greeting - reference to the function
    
myfunction = yet_another_hello_world #provides reference to a function
my_function = yet_another_hello_world()  #invokes the function, so we get a reference to greeting
print(my_function("Jane"))


def increase(x):
    return x+1
    
    
def decrease(x):
    return x-1
   
def square(x)
    return x*x
    
def apply_function_list(func_list, number) #takes in a list of functions and a number
    if (len(func_list)) == 0:
        return number
    else:
        return apply_function_list(func_list[1:],func_list[0](number)) #taking out first element, passing out rest of the list

apply_function_list([increase,decrease,square], 10)

#python decorator

def say_hello(name): 
    return "hello world " + name

def my_decorator(func): #passes in say_hello as a function
    def wrapper():
        name = "jack"
        return func(name) #invokes say_hello passing in name as a parameter 
decorated_function = my_decorator(say_hello) #pass in function as a parameter

print(decorated_function())
#could also do print(decorated_function('jack')) if we didn't assign name to jack

def my_decorator(func):
    def wrapper(name);
        return func(name)
    return wrapper
    
@my_decorator

def say_hello(name):
    return "Hello World" + name
    
say_hello("jack")



#take a base function, e.g. say_hello. We want to decorate this (extend its functionality) 



