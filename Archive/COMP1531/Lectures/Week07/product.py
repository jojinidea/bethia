
from abc import ABC, abstractmethod
class  Product(ABC):
	#class level variable
	__id = 0
	def __init__(self, name, price):
		self._name = name
		self._price = price
		self._code = self.generate_id()
	
	def generate_id(self):
		Product.__id += 1
		return product.__id
	
	#getters and setters
	@property 
	def name(self):
		return _self.name
		
class Clothing(Product):
	def __init__(self, name, price, size, color):
		super().__init__(name,price)  #a reference to a method in the parent class
		self._size = size
		self._color = color
	
	
	@property
	def size(self):
		return _self.size
	
class Camping(Product):
	def __init__(self,name,price, weight, dimension)
		super().__init__(name, price)
		self._dimension = dimension
		
class Shirt(Clothing):
def __init__(self, name, price=0, size = 'S', colour = 'unkown)   #defining some default values.

