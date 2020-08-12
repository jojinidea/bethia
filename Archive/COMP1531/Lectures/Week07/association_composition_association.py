# association - two objects being related - how strong is their relationship
# the car & the person have a very weak relationship as the lifecycles of the car and the person are completely different & independent

class Car
def __init__(self, person) 
    self._person = person 

#instead of this, we would define the constructor without the person
def __init__(self, engine)
    self._engine = engine

    @property setter
        def person
 
#instance of car independent of instance of the person

#what if a car contains an engine - aggregation. The part can exist independently of the container
#if the engine cannot be used without cars, then we would have a composition
class Car
def __init__(self, engine)
    self._engine = engine
    
    
e = Engine()
c1 = Car(e) #example of an aggregation, when we instantiate car, we need to pass in e
c2 = Car(e)
# the above means we can pass in the engine to different car instances (if we destroy c1, can still pass e to c2)


#for compositions, we need to think about if the container is destroyed, the part is destroyed. Instantiation debated

#COMPOSITION

class Engine
def __init__(self, size, chassi)
    self._size = size
    self._chassi = chassi

class Car
def __init__(self, model, size, chassi)
    self._engine = Engine(size, chassi) # ** THIS IS THE LINE that makes sure the engine is always instantiated inside the constructor Car. When the container is instantiated, the part is. If we destroy the car, we destroy the Engine

#the part needs to always be instantiated
c = ("Honda", 4, "xyz")
