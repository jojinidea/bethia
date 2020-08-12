#tackling US2

class Item():
    
    def __init__(self, name, price, avail):
        self._name = name
        self._price = price
        self._avail = avail
        
    def get_name(self):
        return self._name
    
    def get_price(self):
        return self._price
    
    def is_avail(self):
        return self._avail
        
class Menu():

    def __init__(self):
        self._m = []
    
    def get_item(self, name):
        for i in self._m:
            if i.get_name() == name:
                return i
        return None
    
    def add_item(self, name, price, avail):
        self._m.append(Item(name,price,avail))
        
        
class Order():
    
    def __init__(self,item, notes ="") #optional argument to provide notes
        self._item = item;
        self._notes = notes
    
    def get_item(self):
        return self._item
    
    def get_notes(self):
        return self._notes
    
class Table():
    
    def __init__(self, tableid)
        self._tableid = tableid
        self._orders = [] # with lists, you're returning a direct way to modify your internal state. Might have to duplicate list 
        
    def get_orders(self):
        return self._orders
    
    def get_tableid(self):
        return self._tableid
   
    def add_order(self,item,notes="")
        self._orders.append(Order(item, notes))
        
class RestSystem():

    def __init__(self, n_tables, menu):
        self._menu = menu
        self._tables = []
        for i in range(n_tables):
            self._tables.append(Table(i)))
        
    def add_order(self, tableid, name, notes = ""): #if 2 arguments provided, notes will become an empty string, if we provide 3 arguments, third argument will be set to notes
        item = self._menu.get_item(name)
        self._tables[tableid].add_order(item, notes) #assuming all these inputs are valid
        
        
    def get_table_order(self, tableid):
        return self._tables[tableid]


