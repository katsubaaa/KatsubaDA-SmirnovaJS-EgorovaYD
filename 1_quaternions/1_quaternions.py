class Quaternion:
    """Класс кватернионов."""
    def __init__(self, w, x, y, z):
        """Инициализирует объект класса кватернионов."""
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """Вычисляет сложение кватернионов."""
        return Quaternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    def __sub__(self, other):
        """Вычисляет вычитание кватернионов."""
        return Quaternion(self.w - other.w,
                          self.x - other.x,
                          sel f.y - other.y,
                          self.z - other.z)

    def __mul__(self, other):
        """Вычисляет произведение кватернионов."""
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    def scale(self, scalar):
        """Вычисляет произведение кватерниона на скалярную величину."""
        return Quaternion(self.w * scalar, self.x * scalar, self.y * scalar, self.z * scalar)

    def norm(self):
        """Вычисляет норму кватерниона."""
        return (self.w**2 + self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self):
        """Нормализует кватернион (приводит к единичной норме)."""
        norm_value = self.norm()
        if norm_value == 0:
            raise ValueError("Cannot normalize zero quaternion")
        return self.scale(1 / norm_value)

    def dot(self, other):
        """Вычисляет скалярное произведение двух кватернионов."""
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def conjugate(self):
        """Вычисляет конъюгат кватерниона."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self):
        """Вычисляет обратный кватернион."""
        norm_sq = self.norm() ** 2
        if norm_sq == 0:
            raise ZeroDivisionError("Cannot invert zero quaternion")
        return self.conjugate().scale(1 / norm_sq)

    def __repr__(self):
        """Строкое представление объекта класса кватернионов."""
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def rotate(self, vector):
        """Поворот вектора кватернионом."""
        q_vector = Quaternion(0, vector[0], vector[1], vector[2])
        q_conjugate = Quaternion(self.w, -self.x, -self.y, -self.z)
        rotated_vector = self * q_vector * q_conjugate
        return (rotated_vector.x, rotated_vector.y, rotated_vector.z)
