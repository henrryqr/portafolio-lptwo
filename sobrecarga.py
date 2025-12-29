class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, o):
        return Vector2D(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector2D(self.x - o.x, self.y - o.y)

    def __mul__(self, escalar):
        return Vector2D(self.x * escalar, self.y * escalar)

    def __repr__(self):
        return "Vector(" + str(self.x) + "," + str(self.y) + ")"


v1 = Vector2D(2, 3)
v2 = Vector2D(1, 1)
v3 = v1 + v2
v4 = v3 - v2
v5 = v4 * 4

print(v1)
print(v2)
print(v3)
print(v4)
print(v5)
