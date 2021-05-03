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

    def PREPEND(self, other):
        if isinstance(other, List):
            return List([self.value]).ADD(other)

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

    def NOT(self):
        return String(self.value[::-1])

    def PREPEND(self, other):
        if isinstance(other, List):
            return List([self.value]).ADD(other)

    def getBy(self, from_, end):
        try:
            if from_.value == end.value:
                return String(self.value[from_.value])
            return String(self.value[from_.value:end.value])
            
        except IndexError: return String("")

    def setItem(self, index, value):
        lValue              = [*self.value]
        lValue[index.value] = value.value
        self.value          = ''.join(lValue)
        return self

    def length(self):
        return Int(len(self.value))

    def head(self):
        try              : return String(self.value[0])
        except IndexError: return String("")
    
    def tail(self):
        try              : return String(self.value[1:])
        except IndexError: return String("")

    def iter(self):
        for char in self.value:
            yield String(char)
    
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
    
    def EQUAL(self, other):
        if isinstance(other, List):
            return Int(self.elements == other.elements)

    def NOT_EQUAL(self, other):
        if isinstance(other, List):
            return Int(self.elements != other.elements)

    def NOT(self):
        return List(self.elements[::-1])

    def PREPEND(self, other):
        if isinstance(other, List):
            return self.ADD(other)

    def APPEND(self, other):
        self.elements.append(other)
        return self

    def getBy(self, from_, end):
        try:
            if from_.value == end.value:
                return self.elements[from_.value]
            return List(self.elements[from_.value:end.value])

        except IndexError: return List([])

    def setItem(self, index, value):
        self.elements[index.value] = value
        return self

    def length(self):
        return Int(len(self.elements))

    def head(self):
        try              : return self.elements[0]
        except IndexError: return List([])
    
    def tail(self):
        try              : return List(self.elements[1:])
        except IndexError: return List([])

    def iter(self):
        for element in self.elements:
            yield element

    def __repr__(self):
        return "{"+ '; '.join([str(element) for element in self.elements]) +"}"