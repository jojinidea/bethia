from abc import ABC,abstractmethod
class Switch(ABC):
        @abstractmethod
        def isOn():
                pass
        @abstractmethod
        def press():
                pass
        
class Switchable(ABC):
        @abstractmethod
        def turnOn():
                pass
        @abstractmethod
        def turnOff():
                pass

class LightBulb(Switchable):
        def turnOn(self):
                print("turning light on")
        def turnOff(self):
                print("turning light off")

class Fan(Switchable):
        def turnOn(self):
                print("turning fan on")
        def turnOff(self):
                print("turning fan off")


class ElectricSwitch(Switch): #electric switch takes in a device, so the dependency (the type of device) is injected
        def __init__(self, device):
                self._switchable_device = device
                self._on = False

        def isOn(self):
                return self._on

        def press(self):
                on = self.isOn()
                if on:
                        self._switchable_device.turnOff() # dependency inversion - we no longer turn on the light bulb directly
                        self._on = False
                else:
                        self._switchable_device.turnOn()
                        self._on = True

es = ElectricSwitch(LightBulb()) #when we instantiate an instance of the electric switch, we inject in the dependency
es.press() #this is invoking the press on the middle abstraction 

es = ElectricSwitch(Fan())
es.press()
