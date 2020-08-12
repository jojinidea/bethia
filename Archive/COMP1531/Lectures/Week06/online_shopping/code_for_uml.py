# is the sub-class atomic or can it be broken down into more fine-grained/composite attributes
# pants/shirts/jackets are subclasses because they have additional attributes

from abc import ABC, abstractmethod

class Product(ABC):

    __id = 0
    
    def __init__(self,name,price):
        self.name = name
        self.price = price
    #every object will have its unique attributes above. Contrasts with instance variables (only can access the variable with the object instance it belongs to) 
    
    def generate_id(self):
        Product.__id += 1
        return product.__id
    
    @property
    define price(self):
        return _self.price
        
    @property
    define code(self):
        return _self.code
       
    @property
    define name(self):
        return _self.name
    
    def __str__(self):
        return str(self.code) + ":" + self.name + "," + str(self.price)

class Clothing(Product):
    def __init__(self,name,price,size,color):
        super().__init__(name,price)
        self._size = size
        self._color = color
    
    @property
    define size(self):
        return _self.size
        
    @property
    define color(self):
        return _self.color

class Camping(Product):
    def __init__(self,name,price,dimension,weight)
        super().__init__(name,price)
        self._dimension = dimension
        self._weight = weight
        
    p1 = Product()
    p1._name #instance variable
    
    #class variables do not belong to a particular object instance (like a global variable), only ever one copy of that variable (associated at the class variable)  
