from json import dumps

class Token:
    def __init__(self, _type, value, begin, end, line, position):
        self.type  = _type
        self.value = value
        self.begin = begin
        self.end   = end
        self.line  = line
        self.position = position

    def match(self, _type):
        return self.type == _type

    def __repr__(self):
        return str(
            {
                self.type: self.value,
                "begin": self.begin,
                "end": self.end,
                "line": self.line,
                "truePosition": self.position
            }
        )
