class Token:
    def __init__(self, _type, value):
        self.type  = _type
        self.value = value

    def match(self, _type):
        return self.type == _type

    def tree(self):
        return [f'{self.type}: "{self.value}"']


    def __repr__(self):
        return str(
            {
                self.type: self.value
            }
        )
