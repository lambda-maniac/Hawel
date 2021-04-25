class SymbolTable:
    def __init__(self, parent = None):
        self.symbols = {}
        self.parent  = parent 

    def get(self, name):
        value = self.symbols.get(name, None)

        if value == None and self.parent:
            return self.parent.symbols.get(name)

        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

class Context:
    def __init__(self, name, parent = None):
        self.contextName = name
        self.symbolTable = SymbolTable(parent)
