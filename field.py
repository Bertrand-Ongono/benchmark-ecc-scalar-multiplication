# field.py


class FieldOps:
    def __init__(self, p):
        self.p = p
        self.mul_count = 0
        self.inv_count = 0

    def reset(self):
        self.mul_count = 0
        self.inv_count = 0

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        self.mul_count += 1
        return (a * b) % self.p

    def inv(self, a):
        if a % self.p == 0:
            raise ZeroDivisionError("Inversion modulaire impossible pour 0 modulo p")
        self.inv_count += 1
        return pow(a, -1, self.p)