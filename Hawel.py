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
        return f'int::\'{self.token.value}\''

class StringNode:
    def __init__(self, token):
        self.token = token

        self.token.value = self.token.value[1:-1:]

    def __repr__(self):
        return f'string::\'{self.token.value}\''

class UnaryOpNode:
    def __init__(self, operator, node):
        self.operator = operator
        self.node     = node

    def __repr__(self):
        return f'(operate::{self.operator}, to::{self.node})'

class VariableNode:
    def __init__(self, name, valueNode):
        self.name      = name
        self.valueNode = valueNode

    def __repr__(self):
        return f'(set::"{self.name}", as::{self.valueNode})'

class VariableAccessNode:
    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return f'get::{self.variable}'

class BinOpNode:
    def __init__(self, operation, leftNode, rightNode):
        self.operation = operation
        self.leftNode  = leftNode
        self.rightNode = rightNode

    def __repr__(self):
        return f'(do::{self.operation}, to::(left::{self.leftNode}, right::{self.rightNode}))'

class IfNode:
    def __init__(self, cases):
        self.cases = cases

    def __repr__(self):
        return ''.join([f'(if::{condition}, do::{expression})' for condition, expression in self.cases])

class ForNode:
    def __init__(self, variableNameToken, startValueNode, endValueNode, stepValueNode, bodyNode):
        self.variableNameToken = variableNameToken
        self.startValueNode    = startValueNode
        self.endValueNode      = endValueNode
        self.stepValueNode     = stepValueNode
        self.bodyNode          = bodyNode

    def __repr__(self):
        return f'(for::{self.variableNameToken}, as::{self.startValueNode}, to::{self.endValueNode}, by::{self.stepValueNode}, do::{self.bodyNode})'    

class WhileNode:
    def __init__(self, conditionNode, bodyNode):
        self.conditionNode = conditionNode
        self.bodyNode      = bodyNode

    def __repr__(self):
        return f'(while::{self.conditionNode}, do::({self.bodyNode})'

class FunctionDefinitionNode:
    def __init__(self, functionNameToken, argNameTokens, bodyNode):
        self.functionNameToken = functionNameToken
        self.argNameTokens     = argNameTokens
        self.bodyNode          = bodyNode

    def __repr__(self):
        return f'(Funcion::{self.functionNameToken.value}, args::{self.argNameTokens}, body::{self.bodyNode})'

class ReturnNode:
    def __init__(self, nodeToReturn):
        self.nodeToReturn = nodeToReturn

    def __repr__(self):
        return f'return::{self.nodeToReturn}'

class CallNode:
    def __init__(self, nodeToCall, argNodes):
        self.nodeToCall = nodeToCall
        self.argNodes   = argNodes

    def __repr__(self):
        return f'(call::(args::{self.argNodes}, on::{self.nodeToCall}))'

class ListNode:
    def __init__(self, nodeList):
        self.nodeList = nodeList

    def __repr__(self):
        return "{"+'; '.join([str(node) for node in self.nodeList])+"}"

class Parser:
    def __init__(self, tokens):
        self.tokens     = tokens
        self.tokenIndex = -1

        self.advance()

    def parse(self):
        return self.statements()

    def advance(self):
        self.tokenIndex += 1

        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]

    def statements(self):
        statements = []

        statements.append(self.statement())
        while self.currentToken.match("NEXT"):
            self.advance()
            statements.append(self.statement())

        return ListNode(statements)

    def statement(self):
        if self.currentToken.match("RETURN"):
            self.advance()
            return ReturnNode(self.expression())
        return self.expression()

    def binOperation(self, leftTokenType, operations, rightTokenType):
        leftNode = leftTokenType()

        while self.currentToken.type in operations:
            operationToken = self.currentToken

            self.advance()

            rightNode = rightTokenType()
            leftNode  = BinOpNode(operationToken, leftNode, rightNode)

        return leftNode

    def listExpression(self):
        nodesList = []

        if self.currentToken.match("RIGHT_CURLY"):
            self.advance()

        else:
            nodesList.append(self.expression())

            while self.currentToken.type == "SEPARATOR":
                self.advance()

                nodesList.append(self.expression())

            if self.currentToken.type != "RIGHT_CURLY":
                raise SyntaxError(f'Expected ";" or "{"}"}", got Token: {self.currentToken.type}')
            self.advance()
        
        return ListNode(nodesList)

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

        body = self.statements()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected "$", got: "{self.currentToken.type}"')
        self.advance()

        return FunctionDefinitionNode(
            functionName,
            argNameTokens,
            body
        )

    def whileExpression(self):
        condition = self.expression()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        body = self.statements()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        return WhileNode(condition, body)

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

        body = self.statements()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        return ForNode(variableName, startValue, endValue, stepValue, body)

    def ifExpression(self):
        cases     = []

        condition = self.expression()

        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

        cases.append((condition, self.statements()))

        while self.currentToken.match('ELSE_IF'):
            self.advance()

            condition = self.expression()
            
            if not self.currentToken.match("BLOCK"):
                raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
            self.advance()

            cases.append((condition, self.statements()))

        if self.currentToken.match("ELSE"):
            self.advance()

            cases.append((IntNode(Token("INT", 1)), self.statements()))
        
        if not self.currentToken.match("BLOCK"):
            raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
        self.advance()

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
    
    def getArgs(self):
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

        return argNodes

    def call(self):
        atom = self.atom()

        stack  = None
        reduce = False
        while self.currentToken.type == "LEFT_BRACKET":
            argNodes = self.getArgs()

            if reduce: stack = CallNode(stack, argNodes)
            else     : stack = CallNode(atom, argNodes); reduce = True
        
        return stack if stack else atom

    def factor(self):
        token = self.currentToken

        if token.type in "ADD|SUB":
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

        elif token.match("LEFT_CURLY"):
            self.advance()
            return self.listExpression()

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
        self.symbols     = SymbolTable(parent)

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

class RuntimeResult:
    def __init__(self) : self.reset()

    def reset(self):
        self.value = None
        self.error = None

        self.returnValue    = None
        self.shouldBreak    = False
        self.shouldContinue = False
    
    def register(self, response):
        if response.error          : self.error          = response.error
        if response.value          : self.value          = response.value
        if response.returnValue    : self.returnValue    = response.returnValue
        if response.shouldBreak    : self.shouldBreak    = response.shouldBreak
        if response.shouldContinue : self.shouldContinue = response.shouldContinue
        
        return self.value

    def proceed(self, value):
        self.value = value
        return self

    def proceedWithReturn(self, value):
        self.reset()
        self.returnValue = value
        self.value       = value
        return self

    def proceedWithContinue(self):
        self.reset()
        self.shouldContinue = True
        return self

    def proceedWithBreak(self):
        self.reset()
        self.shouldBreak = True
        return self

    def shouldReturn(self):
        return (
            self.error       or 
            self.returnValue or
            self.shouldBreak or 
            self.shouldContinue
        )

    # def failure(self, error):
    #     self.error = error
    #     return self

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
        return RuntimeResult().proceed(
            Int(node.token.value)
        )

    def visitStringNode(self, node, context):
        return RuntimeResult().proceed(
            String(node.token.value)
        )

    def visitListNode(self, node, context):
        response = RuntimeResult()
        
        visitedNodes = []
        for elementNode in node.nodeList:
            
            visitedNode = response.register(self.visit(elementNode, context))
            if response.shouldReturn(): return response

            visitedNodes.append(visitedNode)

        return response.proceed(
            List(visitedNodes)
        )

    def visitVariableAccessNode(self, node, context):
        value = context.symbols.get(node.variable.value)

        if not value:
            raise SyntaxError(f'Variable "{node.variable.value}" not declared.')

        return RuntimeResult().proceed(value)

    def visitUnaryOpNode(self, node, context):
        response = RuntimeResult()

        value = response.register(self.visit(node.node, context))
        if response.shouldReturn(): return response

        if node.operator.type == 'SUB':
            return response.proceed(value.MUL(Int(-1)))

        if node.operator.type == 'NOT':
            return response.proceed(value.NOT())

        # if node.operator.type in 'INCREMENT|DECREMENT':
        #     return response.proceed(getattr(value, node.operator.type)())

        return response.proceed(value)

    def visitVariableNode(self, node, context):
        response = RuntimeResult()

        value = response.register(self.visit(node.valueNode, context))
        if response.shouldReturn(): return response

        context.symbols.set(node.name, value)

        return response.proceed(value)
        
    def visitBinOpNode(self, node, context): ### DEBUGGING ###
        response = RuntimeResult()

        left  = response.register(self.visit(node.leftNode, context))
        if response.shouldReturn(): return response
        
        right = response.register(self.visit(node.rightNode, context))
        if response.shouldReturn(): return response

        return response.proceed(getattr(left, node.operation.type)(right))

    def visitIfNode(self, node, context):
        response = RuntimeResult()

        for condition, expression in node.cases:
            conditionValue = response.register(self.visit(condition, context))
            if response.shouldReturn(): return response

            if conditionValue.value != 0:
                response.register(self.visit(expression, context))
                if response.shouldReturn(): return response
                
                break

        return response.proceed(Int(0))

    def visitForNode(self, node, context):
        response = RuntimeResult()

        startNode = response.register(self.visit(node.startValueNode, context))
        if response.shouldReturn(): return response

        endNode   = response.register(self.visit(node.endValueNode  , context))
        if response.shouldReturn(): return response

        stepNode  = response.register(self.visit(node.stepValueNode , context))
        if response.shouldReturn(): return response

        for iterator in range(startNode.value, endNode.value, stepNode.value):
            context.symbols.set(node.variableNameToken.value, Int(iterator))

            response.register(self.visit(node.bodyNode, context))
            if response.shouldReturn()  : return response
            if response.shouldBreak   : break
            if response.shouldContinue: continue

        return response.proceed(Int(0))

    def visitWhileNode(self, node, context):
        response = RuntimeResult()

        while response.register(self.visit(node.conditionNode, context)).value != 0:

            response.register(self.visit(node.bodyNode, context))
            if response.shouldReturn(): return response
            if response.shouldBreak   : break
            if response.shouldContinue: continue

        return response.proceed(Int(0))

    def visitFunctionDefinitionNode(self, node, context):
        functionName = node.functionNameToken.value
        bodyNode     = node.bodyNode
        
        function = Function(functionName, node.argNameTokens, bodyNode)

        if node.functionNameToken:
            context.symbols.set(functionName, function)

        return RuntimeResult().proceed(function)

    def visitCallNode(self, node, context):
        response = RuntimeResult()

        valueToCall = response.register(self.visit(node.nodeToCall, context))
        if response.shouldReturn(): return response

        args = [response.register(self.visit(argNode, context)) for argNode in node.argNodes]

        return response.proceed(
            valueToCall.execute(args, context)
        )

    def visitReturnNode(self, node, context):
        response = RuntimeResult()

        value = response.register(self.visit(node.nodeToReturn, context))
        if response.shouldReturn(): return response

        return response.proceedWithReturn(value)

    def visitContinueNode(self, node, context):
        return RuntimeResult().proceedWithContinue()

    def visitBreakNode(self, node, context):
        return RuntimeResult().proceedWithBreak()

class Function:
    def __init__(self, name, argNames, bodyNode):
        self.name     = name
        self.argNames = argNames
        self.bodyNode = bodyNode

    def execute(self, args, upperContext):
        if len(args) > len(self.argNames):
            raise SyntaxError(f'Too many arguments given to "{self.name}".')
        if len(args) < len(self.argNames):
            raise SyntaxError(f'Too few arguments given to "{self.name}".')

        context = Context(self.name, upperContext)

        for i in range(len(args)):
            argName  = self.argNames[i].value
            argValue = args[i]
            context.symbols.set(argName, argValue)

        response = RuntimeResult()

        value = response.register(Interpreter(self.bodyNode).interpretate(context))
        if response.shouldReturn() and response.returnValue == None: return response
        
        return response.proceed(value if value else Int(0))

    def __repr__(self):
        return f'<function {self.name}>'

def main():

    import sys

    Tokens = \
    {
        # Ignore
        r"^[\s+\n+]": None,

        # Var
        r"^\-\-": "MAKE_VAR",

        # Return
        r"^\<\<\=": "RETURN",
        r"^continue": "CONTINUE",
        
        # If, Else If, Else
        r"^\?\.\.": "IF",
        r"^\.\?\.": "ELSE_IF",
        r"^\.\.\?": "ELSE",

        # For loop
        r"^\!": "FOR",
        r"^\=\>": "ARROW",
        r"^\.\.": "STEP",

        # Next
        r"^\|": "NEXT",

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
        r"^\{": "LEFT_CURLY",
        r"^\}": "RIGHT_CURLY",

        # Arithmetic
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

    if len(sys.argv) == 1:
        while True:

            tokens = Lexer(Tokens).lex(input(">>> "))
            print(f"\nToken List: {tokens}")

            ast = Parser(tokens).parse()
            print(f'\nAST: {ast}')

            result = Interpreter(ast).interpretate(context)
            print(f'\nresult: {result.value}')

    else:
        with open(f'{sys.argv[1]}', 'r') as file:
            print(Interpreter(Parser(Lexer(Tokens).lex(file.read())).parse()).interpretate(context))

if __name__ == '__main__': main()
