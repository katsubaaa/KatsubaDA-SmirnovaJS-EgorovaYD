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

# Примеры, показывающие нарушение принципа LSP в Square
print("Пример для Square:")
square = Square(5)
print("Изначальная ширина:", square.width)
print("Изначальная высота:", square.height)

square.width = 10
print("После изменения ширины:")
print("Ширина:", square.width)  # 10
print("Высота:", square.height)  # 5 (нарушение)

# Примеры, демонстрирующие выполнение принципа LSP в Square2
print("\nПример для Square2:")
square2 = Square2(5)
print("Изначальная ширина:", square2.width)
print("Изначальная высота:", square2.height)

square2.width = 10
print("После изменения ширины:")
print("Ширина:", square2.width)  # 10
print("Высота:", square2.height)  # 10 (корректное поведение)

square2.height = 7
print("После изменения высоты:")
print("Ширина:", square2.width)  # 7
print("Высота:", square2.height)  # 7 (корректное поведение)
