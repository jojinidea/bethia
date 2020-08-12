class Vehicle(ABC):
    @abstractmethod:
    def move(self):
        pass

class Car(Vehicle):
    def move(self):
        print("Car moving...")
        
class Bike(Vehicle):
    def move(self):
        print("Bike moving...")
        
class Traveller():
    def __init__(self):
        pass
        
    def start_journey(self, Vehicle):
        Vehicle.move()
        
        
# design problem is that the high level module (traveller) is directly dependent on the low-level module (Car/Bike). This does not conform to the SOLID principles as there is extremely high coupling between these two modules (i.e. any internal changes to the low level modules will directly affect the ability of the high level module to execute the function start_journey)

# both classes should instead, depend on an intermediate abstraction layer. We can implement this by creating an abstract class - Vehicle and having Car and Bike inherit from the class Vehicle

#we can then inject the dependency via an abstract class into the function - start journey, which relies upon the dependency.


