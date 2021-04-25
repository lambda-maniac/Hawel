class Int:
    def __init__(self, value):
        self.value = value

    def ADD(self, other):
        if isinstance(other, Int):
            return Int(self.value + other.value)

    def SUB(self, other):
        if isinstance(other, Int):
            return Int(self.value - other.value)

    def MUL(self, other):
        if isinstance(other, Int):
            return Int(self.value * other.value)

    def DIV(self, other):
        if isinstance(other, Int):
            return Int(self.value / other.value)

    def POW(self, other):
        if isinstance(other, Int):
            return Int(self.value ** other.value)

    def INCREMENT(self):
        return Int(self.value + 1)

    def DECREMENT(self):
        return Int(self.value - 1)

    def GREATER_THAN(self, other):
        if isinstance(other, Int):
            return Int(self.value > other.value)

    def GREATER_THAN_OR_EQUAL(self, other):
        if isinstance(other, Int):
            return Int(self.value >= other.value)

    def LESS_THAN(self, other):
        if isinstance(other, Int):
            return Int(self.value < other.value)

    def LESS_THAN_OR_EQUAL(self, other):
        if isinstance(other, Int):
            return Int(self.value <= other.value)

    def EQUAL(self, other):
        if isinstance(other, Int):
            return Int(self.value == other.value)

    def NOT_EQUAL(self, other):
        if isinstance(other, Int):
            return Int(self.value != other.value)

    def AND(self, other):
        if isinstance(other, Int):
            return Int(self.value and other.value)

    def OR(self, other):
        if isinstance(other, Int):
            return Int(self.value or other.value)

    def NOT(self):
        return Int(not self.value)

    def __repr__(self):
        return f'{self.value}'

class String:
    def __init__(self, value):
        self.value = value

    def ADD(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)

    def MUL(self, other):
        if isinstance(other, Int):
            return String(self.value * other.value)

    def DIV(self, other):
        if isinstance(other, Int):
            return String(self.value[other.value:])

    def EQUAL(self, other):
        if isinstance(other, String):
            return Int(self.value == other.value)

    def NOT_EQUAL(self, other):
        if isinstance(other, String):
            return Int(self.value != other.value)
    
    def __repr__(self):
        return f'{self.value}'

class List:
    def __init__(self, elements):
        self.elements = elements

    def ADD(self, other):
        if isinstance(other, List):
            return List(self.elements + other.elements)

    def POW(self, other):
        if isinstance(other, Int):
            return self.elements.pop(other.value)

    def __repr__(self):
        return "{"+'; '.join([str(element) for element in self.elements])+"}"
