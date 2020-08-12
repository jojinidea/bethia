from abc import ABC, abstractmethod

class Shape(ABC):

    def __init__(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def __str__(self):
        return self._color

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def scale(self, ratio):
        pass

class Rectangle(Shape):

    def __init__(self, color, width,height):
        super().__init__(color)
        self._width = width
        self._height = height

    def get_width():
            return self._width;

    def set_width(width):
            self._width = width;

    def get_height():
            return self._height;

    def set_height(height):
            self._height = height;

    def area(self):
        return self._height * self._width

    def scale(self, ratio):
        self._width *= ratio
        self._height *= ratio

    def __str__(self):
        return super().__str__() + " rectangle with area {0}".format(self.area())

class Circle(Shape):

    def __init__(self, color, radius):
        Shape.__init__(self,color)
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        
        self._radius = radius

    def area(self):
        return 3.14 * self._radius * self._radius

    def scale(self, ratio):
        self._radius *= ratio

    def __str__(self):
        return super().__str__() + " circle with area {0}".format(self.area())

shape1 = Rectangle('red',5,6)
shape2 = Circle('blue',4)

print(shape1)
print(shape2)

