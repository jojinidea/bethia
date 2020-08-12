#python object oriented programming

class Employee: #employee class with no attributes or methods
    def __init__(self, first, last, pay): #we can also specify what other arguments we want each instance of the class to accept 
    self.first = first
    self.last = last
    self.pay = pay
    self.email = first + '.' + last + '@company.com'
    
    def fullname(self): #method within the class
        return '{} {}'.format(self.first, self.last) #will print each instance's first name and their last name

#with init, we can pass in the arguments into the Employee(), which will automatically set these values

emp_1 = Employee("Name", "Last_name", "6000") #employee 1 is passed in as self, and then init will set all the other attributes - "name" as first, "Last_name" as last, "6000" as pay
emp_2 = Employee("Name2", "Last_name2", "7000")


print(emp_1.fillname()) #need () as this is a method
# don't need to pass in self, if we call the method with an instance it works
# essentially gets transformed into Employee.fullname(emp_1)

Employee.fullname(emp_1) #need to pass in the instance if we use it through the class

#we can create a method within our class that puts functionaltiy in place

