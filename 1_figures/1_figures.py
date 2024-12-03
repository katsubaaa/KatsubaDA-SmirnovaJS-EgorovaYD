class Shape:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle(Shape): 
    def __init__(self, width, height, x=0, y=0): 
        super().__init__(x, y)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)
        
class Square2(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = self._height = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._width = self._height = value
