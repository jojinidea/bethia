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
                updated_msg = greeting_class._message + " There" #alters message variable in greeting class directly. If we change the greeting_class.message to be a dictionary, the tightly coupled class will be affected. We will need to make changes here as well
                #changes to greeting class will impact the calling module
                greeting_class._message = updated_msg
                print(greeting_class._message)
                
class Loosely_Coupled_Class():

        def do_something():
                greeting_class = Greeting_Class()
                updated_msg = greeting_class.get_message() + " There" #if we change self._message to be a dictionary, we would have to change get_message. But the Loosely_Coupled_Class is not impacted by these changes
                greeting_class.set_message(updated_msg)
                print(greeting_class.get_message())
                

Tightly_Coupled_Class.do_something()
