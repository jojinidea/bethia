import pytest
#need to import any classes you're testing
from classes import * #import everything

def test_simple_arith(): #defining a function that starts with string test, might have to activate virtual env
    assert 4 + 5 == 9


class TestUS1(): #pytest sees this, interprets it as a set of test-cases
    def setup_class(self): #executed once, before any of your test-cases
        pass
    
    def setup_method(self): #execute once before any of test-cases
        #self.x = 2
        self.menu = Menu()
        self.menu.add_item("Burger", 20, True)
        self.menu.add_item("Waffles", 5, True)
        self.menu.add_item("Kebab", 50, False)
        self.rest = RestSystem(6, self.menu)
 
    #this happens everytime after every test case - get fresh set of data each time
    #should also test cases with invalid inputs
    
    def teardown_class(self):
        pass
    
    def teardown_method(self):
        pass
    
    def test_adding_order_for_table_id(self):
        self.rest.add_order(0, "Burger")
        #okay to use private attributes to ensure internal state of objects is consistent
        orders = self.rest.get_tables_orders(0)
        item = orders[0].get_item()
        
        assert item.get_name() == "Burger"        
    
    def test_adding_notes(self):
        self.rest.add_order(0, "Waffles", "Nutella on top")
        orders = self.rest.get_table_orders(0)
        assert (orders[0].get_notes() == "Nutella on top")
        
    def test_simple_case(self):
        assert(self.x == 2)
        self.x+=30
    
    # set up method always runs again - so self.x will become 2 (line 11)
    def test_less_simple_case(self):
        assert(self.x + 20 == 22)
        
    
    

