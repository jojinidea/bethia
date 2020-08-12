from product import *
import pickle

class Warehouse():
    def __init__(self):
        self._items

# if we add @pytest.fixture, this means everything defined in a function can be used in test
# testing if a particular list has the elements I want
# b is the list of items returned by the search (each one is an instance of the class product) 
# assert(x.name in a for x in b)
# for every product in the search result (b), extract the name (each instance of x has a name)
# x.name extracts the name  
# does this x.name exist in [a]? 

#search of products by name
def test_general_search_all_by_name(warehouse_fixture):
    text = "Cool"
    result = warehouse_fixture.search_all(text)
    
    for i in result: 
        assert(text in i.name)

#asserts that the string 'text' occurs in every element in result  

#pickle
def save_data(self):
    with open('warehouse.dat', 'wb') as file:
        pickle.dump(self.file) #dumps object instances that exist in memory in a binary format into the file
        
def load_data(self):
    with open('warehouse.dat', 'rb') as file:
        warehouse = pickle.load(file)
    return warehouse
    
#to test
warehouse_fixture.save_data()
loaded_wh = warehouse_fixture.load_data()
a = set(warehouse_fixture.search())
b = set(warehouse_fixture.search())
assert(x in a for x in b) 
  
