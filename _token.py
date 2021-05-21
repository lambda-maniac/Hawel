class Token:
    def __init__(self, _type, value, begin, end, line, position):
        self.type     = _type
        self.value    = value
        self.begin    = begin
        self.end      = end
        self.line     = line
        self.position = position

    def match(self, _type):
        return self.type == _type

    def tree(self):
        return [f'{self.__repr__()}']

    def __repr__(self):
        return f'({self.type}, {self.value})'