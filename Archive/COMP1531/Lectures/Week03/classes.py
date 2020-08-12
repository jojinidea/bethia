class Account(object):
    'A basic account object'
    def__init__(self), name = "", min_bal = 100): #this initialises all the values to default values
    self._min_bal = min_bal #represent 3 attributes in the class account
    self._name = name
    self._balance = min_bal
    
    def despoit(self, amount):
        self.balance += amount
    
    #when defining an instance - first parameter must always be self
    
    # self is the reference to the object instances
    
    # constructor (lines 3-6) initialises values in the
    # self is a reference to the object instance
    
    a1 = Account("John", 50) #creates two instances of the class account
    a2 = Account("Mary", 100) #personalises the values - if we don't do this, they are their default values
    
    # LHS - variable. RHS - insatiation 
    # reference to the block of memory given to the variable 
    # a1 is not the object instance - pointer to the memory

# python will allocate space in memory to store data associated with object instances
# python calculates the amount of space needed for each data type within the class

# to access variables pointed to by a1, we use a1.name/a1.balance
