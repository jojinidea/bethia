from abc import ABC, abstractmethod #imports module

# class Account(ABC):
# sub-classes can include an implementation of a method in the parent class
# e.g. 

class Account(object):
        
    def __init__(self, name, min_bal): #if we pass in variables to init, we can pass them in when we create a class instance
        self._name = name
        self._balance = min_bal #we can define these values to some default values
        # using the underscore is python's way of saying please don't access these variables directly

    def get_balance(self):
        return self._balance
    
    def withdraw(sel, amount):
        if self.balance > amount:
            self.balance -= amount

class SavingsAccount(Account): #defines a subclass - specify base class/parent class in () - initialise variables in parent class by invoking superconstructor
    def__init__(self,name,amount):
        Account.__init__(self,name,amount) #inherits variables from class Account -  a call to the superconstructor (like a function)
        self._saver_interest = 0.05 #initialise specific variable 

a1 = Account("Joe", 50000)
    
print("{0}'s balance is: {1}".format(a1._name, a1.get_balance())) #to access object variables, we have to use this format

# to encapsulate, we want to replace direct access e.g. a1._balance with functions like a1.get_balance()
# can also hide any internal changes 



