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


class ElectricSwitch(Switch):
        def __init__(self, device):
                self._switchable_device = device
                self._on = False

        def isOn(self):
                return self._on

        def press(self):
                on = self.isOn()
                if on:
                        self._switchable_device.turnOff()
                        self._on = False
                else:
                        self._switchable_device.turnOn()
                        self._on = True

es = ElectricSwitch(LightBulb())
es.press()

es = ElectricSwitch(Fan())
es.press()
