#to define an abstract class, we need to import two things from a library called abc

from abc import ABC, abstractmethod 

class Shape(ABC): #extending ABC defines the abstract class
    
    def__init__(self,color): ##need to define constructor
        self._color = color
        
    def get_color(self):
        return self._color
        
    @abstractmethod ## need this to tell Python this is an abstract method
    def get_area(self):
        pass
        
    @abstractmethod
    def scale(self):
        pass
        
    
    ##can also have a str method in Shape
        
#another example
        
class Manager(Employee):
    def __init__(self,name,eid,mid):
        super().__init__(name,eid)
        self._mid = mid    



class Rectangle(Shape): 
    def __init__(self, height, width, color): ##initialisation method with arguments that will be assigned as attributes. Explicit reference to self must also be included
        super().__init__(color) #need to pass in this via the constructor of the parent class
        self._height = height
        self._width = width ## goes to that object, sets its width as the argument of the function 
    ## if an internal attribute begins with an underscore - private

    def get_height(self):
        return self.height
    
    def get_area(self):
        return self._height * self._width
        
    def scale(self,scalar):
        self._height*=scalar
        self._width*=scalar
    
    def __str__(self):
        return "%d %d %s" % (self._height, self._width self._color)
        
    ## override the string method of an object to return this, not the location of the object
        
    #defines abstract methods - implementation not in parent class, can be written in children
    
    
class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color) ##points to the Shape's init
        self._radius = radius
        
    def get_area(self):
        return (self._radius ** 2) * 3.1415
    
    def scale(self, scalar): 
        self._radius = self._radius * scalar
        
    
    def set_radius(self, radius):
        if(radius >= 0): 
            return print("Radius is less than 0")
        else:
            self._radius = radius 
        
class ShapeSystem(): 
    def __init__(self):
        self._allshapes = []
        self._max = 100 #total area less than 100
    
    def add_shape(self, shape): 
        if (self._get_total_area() + shape.get_area() > self._max):
            return False
        else: 
            self.allshapes.append(shape)
            return True

    def _get_total_area(self):
        total_sum = 0
        for shape in self._allshapes:
            total_sum = shape.get_area() + total_sum 
        return total_sum
    
    def print_shapes(self):
        for shape in self._allshapes:
            print(shape)

x = ShapeSystem()
s1 = Rectangle(5,6, "Blue")
s2 = Rectangle(6,10, "Blue")
s3 = Circle(2, 2, "Blue")
s4 = Rectangle(5,4, "Blue")

print(x.add_shape(s1))
print(x.add_shape(s2))
print(x.add_shape(s3))
print(x.add_shape(s4))

x.print_shapes()

#good idea to comment the types of each attribute (e.g. int, string) 
