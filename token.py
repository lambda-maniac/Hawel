from json import dumps

class Token:
    def __init__(self, _type, value):
        self.type  = _type
        self.value = value

    def match(self, _type):
        return self.type == _type

    def __repr__(self):
        return str(
            {
                self.type: self.value
            }
        )
