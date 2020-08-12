class Multiply():
        def multiply(self, a, b):
                return a*b

        def display(self): #don't need display here, because the purpose of the Multiply function is to multiply 2 numbers. Should break away these two functions
                print(self.multiply(5,5))
 

pdt = Multiply()
pdt.display()
