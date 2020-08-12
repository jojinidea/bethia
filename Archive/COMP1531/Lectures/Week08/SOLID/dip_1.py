class LightBulb():
        def turnOn(self):
                print("turning light on")
        def turnOff(self):
                print("turning light off")

#High-level module ElectricSwitch is directly dependent on
#Low-level module light-bulb
class ElectricSwitch():
        def __init__(self, bulb):
                self._lightbulb = bulb
                self._on = False

        def isOn(self):
                return self._on

        def press(self):
                on = self.isOn()
                if on:
                        self._lightbulb.turnOff()
                        self._on = False
                else:
                        self._lightbulb.turnOn()
                        self._on = True

es = ElectricSwitch(LightBulb())
es.press()
