class Token:
    def __init__(self, _type, value):
        self.type  = _type
        self.value = value

    def match(self, _type):
        return self.type == _type

    def __repr__(self):
        return f'["{self.value}": {self.type}]'

class Lexer:
    import re

    def __init__ (self, tokens):
        self.tokens = tokens

    def lex(self, string):
        self.string = string
        self.cursor = 0

        tokenList = []

        while self.cursor < len(self.string):

            tokenFailSafe = 0

            for token, _type in self.tokens.items():
                match = self.re.findall(token, self.string[self.cursor:])

                if match == []: 
                    
                    if (tokenFailSafe := tokenFailSafe + 1) == len(self.tokens):
                        raise SyntaxError (f'Invalid Token: "{self.string[self.cursor]}"')
                    
                    continue
            
                self.cursor += len(match[0])
            
                if _type == None: continue
            
                tokenList.append(Token(_type, match[0]))

        return tokenList

class IntNode:
    def __init__(self, token):
        self.token = token

        self.token.value = int(self.token.value)

    def __repr__(self):
        return f'{self.token}'

class StringNode:
    def __init__(self, token):
        self.token = token

        self.token.value = self.token.value[1:-1:]

    def __repr__(self):
        return f'{self.token}'

class UnaryOpNode:
    def __init__(self, operator, node):
        self.operator = operator
        self.node     = node

    def __repr__(self):
        return f'({self.operator}, {self.node})'

class VariableNode:
    def __init__(self, name, valueNode):
        self.name      = name
        self.valueNode = valueNode

    def __repr__(self):
        return f'({self.name}: {self.valueNode})'

class VariableAccessNode:
    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return f'{self.variable}'

class BinOpNode:
    def __init__(self, operation, leftNode, rightNode):
        self.operation = operation
        self.leftNode  = leftNode
        self.rightNode = rightNode

    def __repr__(self):
        return f'({self.operation}, {self.leftNode}, {self.rightNode})'

class IfNode:
    def __init__(self, cases):
        self.cases = cases

    def __repr__(self):
        return ''.join([f'(? {condition}<<{expression}>>)' for condition, expression in self.cases])

class ForNode:
    def __init__(self, variableNameToken, startValueNode, endValueNode, stepValueNode, bodyNode):
        self.variableNameToken = variableNameToken
        self.startValueNode    = startValueNode
        self.endValueNode      = endValueNode
        self.stepValueNode     = stepValueNode
        self.bodyNode          = bodyNode

    def __repr__(self):
        return f'({self.variableNameToken}: {self.startValueNode} => {self.endValueNode} .. {self.stepValueNode})<<{self.bodyNode}>>'    

class WhileNode:
    def __init__(self, conditionNode, bodyNode):
        self.conditionNode = conditionNode
        self.bodyNode      = bodyNode

    def __repr__(self):
        return f'({self.conditionNode})<<{self.bodyNode}>>'

class FunctionDefinitionNode:
    def __init__(self, functionNameToken, argNameTokens, bodyNode):
        self.functionNameToken = functionNameToken
        self.argNameTokens     = argNameTokens
        self.bodyNode          = bodyNode

    def __repr__(self):
        return f'({self.functionNameToken}({self.argNameTokens})<<{self.bodyNode}>>)'

class CallNode:
    def __init__(self, nodeToCall, argNodes):
        self.nodeToCall = nodeToCall
        self.argNodes   = argNodes

    def __repr__(self):
        return f'({self.nodeToCall}({self.argNodes}))'

class Parser:
    def __init__(self, tokens):
        self.tokens     = tokens
        self.tokenIndex = -1

        self.advance()

    def parse(self):
        return self.expression()

    def advance(self):
        self.tokenIndex += 1

        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]

    def binOperation(self, leftTokenType, operations, rightTokenType):
        leftNode = leftTokenType()

        while self.currentToken.type in operations:
            operationToken = self.currentToken

            self.advance()

            rightNode = rightTokenType()
            leftNode  = BinOpNode(operationToken, leftNode, rightNode)

        return leftNode

    def functionExpression(self):
        if self.currentToken.type == "IDENTIFIER":
            functionName = self.currentToken
            self.advance()

            if not self.currentToken.match("LEFT_BRACKET"):
                raise SyntaxError(f'Expected Token: "[", got Token: "{self.currentToken.type}"')
        else:
            functionName = Token("IDENTIFIER", "<Anonymous>")

            if not self.currentToken.match("LEFT_BRACKET"):
                raise SyntaxError(f'Expected IDENTIFIER or "[", got Token: "{self.currentToken.type}"')
        self.advance()

        argNameTokens = []
        if self.currentToken.type == "IDENTIFIER":
            argNameTokens.append(self.currentToken)
            self.advance()

            while self.currentToken.type == "SEPARATOR":
                self.advance()

                if self.currentToken.type != "IDENTIFIER":
                    raise SyntaxError(f'Expected IDENTIFIER, got: "{self.currentToken.type}"')

                argNameTokens.append(self.currentToken)
                self.advance()

            if not self.currentToken.match("RIGHT_BRACKET"):
                raise SyntaxError(f'Expected ";" or "]", got Token: "{self.currentToken.type}"')
            self.advance()

        else:
            if not self.currentToken.match("RIGHT_BRACKET"):
                raise SyntaxError(f'Expected IDENTIFIER or "]", got Token: "{self.currentToken.type}"')
            self.advance()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected "$", got: "{self.currentToken.type}"')
        self.advance()

        return FunctionDefinitionNode(
            functionName,
            argNameTokens,
            self.expression()
        )


    def whileExpression(self):
        condition = self.expression()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        return WhileNode(condition, self.expression())

    def forExpression(self):
        if self.currentToken.type != "IDENTIFIER":
            raise SyntaxError(f'Expected IDENTIFIER, got: "{self.currentToken.type}"')
        variableName = self.currentToken
        self.advance()

        if self.currentToken.type != "ASSIGNMENT":
            raise SyntaxError(f'Expected Token: ":", got Token: "{self.currentToken.type}"')
        self.advance()

        startValue = self.expression()

        if self.currentToken.type != "ARROW":
            raise SyntaxError(f'Expected Token: "=>", got Token: "{self.currentToken.type}"')
        self.advance()

        endValue = self.expression()

        if self.currentToken.match("STEP"):
            self.advance()

            stepValue = self.expression()

        else: stepValue = IntNode(Token("INT", 1))

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        return ForNode(variableName, startValue, endValue, stepValue, self.expression())

    def ifExpression(self):
        cases     = []

        condition = self.expression()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        cases.append((condition, self.expression()))

        while self.currentToken.match('ELSE_IF'):
            self.advance()

            condition = self.expression()
            
            if not self.currentToken.match("BLOCK"):
                raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
            self.advance()

            cases.append((condition, self.expression()))

        if self.currentToken.match("ELSE"):
            self.advance()

            cases.append((IntNode(Token("INT", 1)), self.expression()))

        return IfNode(cases)

    def arithmeticExpression(self):
        return self.binOperation(self.term, "ADD|SUB", self.term)

    def comparisonExpression(self):
        if self.currentToken.match("NOT"):
            operation = self.currentToken
            self.advance()

            return UnaryOpNode(operation, self.comparisonExpression())

        return self.binOperation(self.arithmeticExpression, "GREATER_THAN|LESS_THAN|GREATER_THAN_OR_EQUAL|LESS_THAN_OR_EQUAL|EQUAL|NOT_EQUAL", self.arithmeticExpression)

    def expression(self):
        if self.currentToken.match("MAKE_VAR"):
            self.advance()

            if self.currentToken.type != "IDENTIFIER":
                raise SyntaxError(f'Expected Identifier Token, got: {self.currentToken.type}.')

            variableName = self.currentToken.value
            self.advance()

            if self.currentToken.type != "ASSIGNMENT":
                raise SyntaxError(f'Expected ":" Token, got: {self.currentToken} of type {self.currentToken.type}.')
            self.advance()

            return VariableNode(variableName, self.expression())

        return self.binOperation(self.comparisonExpression, "AND|OR", self.comparisonExpression)

    def term(self):
        return self.binOperation(self.factor, "MUL|DIV", self.factor)

    def power(self):
        return self.binOperation(self.call, "POW", self.factor)

    def call(self):
        atom = self.atom()

        if self.currentToken.type == "LEFT_BRACKET":
            self.advance()

            argNodes = []
            if self.currentToken.type == "RIGHT_BRACKET":
                self.advance()
            else:
                argNodes.append(self.expression())
                while self.currentToken.type == "SEPARATOR":
                    self.advance()

                    argNodes.append(self.expression())

                if self.currentToken.type != "RIGHT_BRACKET":
                    raise SyntaxError(f'Expected ";" or "]", got Token: {self.currentToken.type}')
                self.advance()
        
            return CallNode(atom, argNodes)

        return atom

    def factor(self):
        token = self.currentToken

        if token.type in "ADD|SUB":
            self.advance()
            return UnaryOpNode(token, self.factor())

        if token.type in "INCREMENT|DECREMENT":
            self.advance()
            return UnaryOpNode(token, self.factor())

        return self.power()

    def atom(self):
        token = self.currentToken

        if token.type == 'INT':
            self.advance()
            return IntNode(token)

        if token.type == 'STRING':
            self.advance()
            return StringNode(token)

        elif token.type == "IDENTIFIER":
            self.advance()
            return VariableAccessNode(token)

        elif token.type == 'LEFT_PARENTHESIS':
            self.advance()
            expression = self.expression()

            if self.currentToken.type == 'RIGHT_PARENTHESIS':
                self.advance()
                return expression

            else:
                raise SyntaxError (f'Expected Token: ")", got Token: "{self.currentToken.type}"')

        elif token.match("IF"):
            self.advance()
            return self.ifExpression()

        elif token.match("FOR"):
            self.advance()
            return self.forExpression()

        elif token.match("WHILE"):
            self.advance()
            return self.whileExpression()

        elif token.match("FUNCTION"):
            self.advance()
            return self.functionExpression()

        raise SyntaxError(f'Unexpected Token: "{token.type}"')

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent  = None

    def get(self, name):
        value = self.symbols.get(name, None)

        if value == None and self.parent:
            return self.parent.get(name)

        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

class Context:
    def __init__(self, name, parent = None):
        self.contextName = name
        self.symbols     = SymbolTable()
        self.parent      = parent

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

class Interpreter:
    def __init__(self, rootNode):
        self.rootNode = rootNode

    def interpretate(self, context):
        return self.visit(self.rootNode, context)

    def visit(self, node, context):
        return getattr(self, f'visit{type(node).__name__}', self.NoVisitMethodNameDeclared)(node, context)

    def NoVisitMethodNameDeclared(self, node, context):
        raise Exception(f'No visit method for {type(node).__name__} declared')

    def visitIntNode(self, node, context):
        return Int(node.token.value)

    def visitStringNode(self, node, context):
        return String(node.token.value)

    def visitVariableAccessNode(self, node, context):
        value = context.symbols.get(node.variable.value)

        if not value:
            raise SyntaxError(f'Variable "{node.variable.value}" not declared.')

        return value

    def visitUnaryOpNode(self, node, context):
        value = self.visit(node.node, context)

        if node.operator.type == 'SUB':
            return value.MUL(Int(-1))

        if node.operator.type == 'NOT':
            return value.NOT()

        if node.operator.type in 'INCREMENT|DECREMENT':
            return getattr(value, node.operator.type)()

        return value

    def visitVariableNode(self, node, context):
        value = self.visit(node.valueNode, context)

        context.symbols.set(node.name, value)

        return value
        
    def visitBinOpNode(self, node, context):
        left  = self.visit(node.leftNode, context)
        right = self.visit(node.rightNode, context)

        return getattr(left, node.operation.type)(right)

    def visitIfNode(self, node, context):
        for condition, expression in node.cases:
            conditionValue = self.visit(condition, context)

            if conditionValue.value != 0:
                return self.visit(expression, context)

        return None

    def visitForNode(self, node, context):
        startNode = self.visit(node.startValueNode, context)
        endNode   = self.visit(node.endValueNode  , context)
        stepNode  = self.visit(node.stepValueNode , context)

        for iterator in range(startNode.value, endNode.value, stepNode.value):
            context.symbols.set(node.variableNameToken.value, Int(iterator))

            self.visit(node.bodyNode, context)

        return None

    def visitWhileNode(self, node, context):
        while self.visit(node.conditionNode, context).value != 0:
            self.visit(node.bodyNode, context)

        return None

    def visitFunctionDefinitionNode(self, node, context):
        functionName = node.functionNameToken.value
        bodyNode     = node.bodyNode
        
        functionValue = Function(functionName, node.argNameTokens, bodyNode)

        if node.functionNameToken:
            context.symbols.set(functionName, functionValue)

        return functionValue

    def visitCallNode(self, node, context):
        valueToCall = self.visit(node.nodeToCall, context)

        args = [self.visit(argNode, context) for argNode in node.argNodes]

        return valueToCall.execute(args)

class Function:
    def __init__(self, name, argNames, bodyNode):
        self.name     = name
        self.argNames = argNames
        self.bodyNode = bodyNode

    def execute(self, args):
        if len(args) > len(self.argNames):
            raise SyntaxError(f'Too many arguments given to {self.name}.')
        if len(args) < len(self.argNames):
            raise SyntaxError(f'Too few arguments given to {self.name}.')

        context = Context(self.name)
        for i in range(len(args)):
            argName  = self.argNames[i].value
            argValue = args[i]
            context.symbols.set(argName, argValue)

        return Interpreter(self.bodyNode).interpretate(context)

    def __repr__(self):
        return f'<function {self.name}>'

def main():

    Tokens = {

        # Ignore
        r"^\s+": None,

        # Var
        r"^\\": "MAKE_VAR",
        
        # If, Else If, Else
        r"^\?\.\.": "IF",
        r"^\.\?\.": "ELSE_IF",
        r"^\.\.\?": "ELSE",

        # For loop
        r"^\!": "FOR",
        r"^\=\>": "ARROW",
        r"^\.\.": "STEP",

        # While loop
        r"^\%": "WHILE",

        # Functions
        r"^\@": "FUNCTION",
        r"^\;": "SEPARATOR",
        r"^\[": "LEFT_BRACKET",
        r"^\]": "RIGHT_BRACKET",
        
        # Syntax
        r"^\$": "BLOCK",

        # Generics
        r"^\d+": "INT",
        r'^"[^"]*"': "STRING",
        r"^[a-zA-Z_\']*[a-zA-Z0-9\']+": "IDENTIFIER",

        # Symbols #
        r"^\:": "ASSIGNMENT",

        # Arithmetic
        r"^\+\+": "INCREMENT",
        r"^\-\-": "DECREMENT",
        r"^\-": "SUB",
        r"^\+": "ADD",
        r"^\*": "MUL",
        r"^\/": "DIV",
        r"^\^": "POW",
        r"^\(": "LEFT_PARENTHESIS",
        r"^\)": "RIGHT_PARENTHESIS",
        

        # Logic 
        r"^\>\=": "GREATER_THAN_OR_EQUAL",
        r"^\<\=": "LESS_THAN_OR_EQUAL",

        r"^\>": "GREATER_THAN",
        r"^\<": "LESS_THAN",

        
        r"^\=\=": "EQUAL",
        r"^\~\=": "NOT_EQUAL",

        r"^\~": "NOT",
        r"^\&\&": "AND",
        r"^\|\|": "OR",
    }

    # Setup Context
    constants = \
    {
        'null': Int(0),
        'pi'  : Int(3.14159265368979),
    }

    context = Context('main')
    for name, value in constants.items():
        context.symbols.set(name, value)
    
    while True:

        tokens = Lexer(Tokens).lex(input(">>> "))

        print("\nToken List: ")
        for token in tokens: print(f'-- {token}')

        ast = Parser(tokens).parse()
        print(f'\nAST: {ast}')

        result = Interpreter(ast).interpretate(context)
        print(f'\nResult: {result} - {type(result)}')

if __name__ == '__main__': main()
