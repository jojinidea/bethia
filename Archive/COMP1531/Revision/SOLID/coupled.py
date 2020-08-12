class Greeting_Class():
        def __init__(self):
                self._message = "hello"

        def get_message(self):
                return self._message

        def set_message(self,msg):
                self._message = msg

#An example of high-coupling, as tightly_coupled_class alters
#message variable in greeting_class directly
#exposed to the internal structure of the class
                
class Tightly_Coupled_Class():

        def do_something():
                greeting_class = Greeting_Class()
                updated_msg = greeting_class._message + " There"
                greeting_class._message = updated_msg
                print(greeting_class._message)
                
class Loosely_Coupled_Class():

        def do_something():
                greeting_class = Greeting_Class()
                updated_msg = greeting_class.get_message() + " There"
                greeting_class.set_message(updated_msg)
                print(greeting_class.get_message())
                

Tightly_Coupled_Class.do_something()
