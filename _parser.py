from _token import Token
from nodes  import *

class Parser:
    def __init__(self, tokens):
        self.tokens       = tokens
        self.tokenIndex   = -1
        self.currentToken = Token("INT", "0")

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

        if self.currentToken.match("CONTINUE"):
            self.advance()
            return ContinueNode()

        if self.currentToken.match("BREAK"):
            self.advance()
            return BreakNode()

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
            functionName = Token("IDENTIFIER", "Anonymous")

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
            if self.currentToken.type != "OF":
                raise SyntaxError(f'Expected Token: ":" or ";;", got Token: "{self.currentToken.type}"')
            self.advance()
            
            iterable = self.expression()

            if not self.currentToken.match("BLOCK"):
                raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
            self.advance()

            body = self.statements()

            if not self.currentToken.match("BLOCK"):
                raise SyntaxError(f'Expected Token: "$", got Token: "{self.currentToken.type}"')
            self.advance()

            return ForEachNode(variableName, iterable, body)

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

    def ternaryExpression(self):
        condition = self.expression()

        if not self.currentToken.match("SWITCH"):
            raise SyntaxError(f'Expected Token: "--", got Token: "{self.currentToken.type}"')
        self.advance()

        caseTrue = self.expression()

        if not self.currentToken.match("SWITCH"):
            raise SyntaxError(f'Expected Token: "--", got Token: "{self.currentToken.type}"')
        self.advance()

        caseFalse = self.expression()

        # if not self.currentToken.match("END_TERNARY"):
        #     raise SyntaxError(f'Expected Token: ";;", got Token: "{self.currentToken.type}"')
        # self.advance()

        return TernaryNode(condition, caseTrue, caseFalse)

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
        return self.binOperation(self.term, "ADD|SUB|PREPEND|APPEND", self.term)

    def comparisonExpression(self):
        if self.currentToken.match("NOT"):
            operation = self.currentToken
            self.advance()

            return UnaryOpNode(operation, self.comparisonExpression())

        return self.binOperation(self.arithmeticExpression, "GREATER_THAN|LESS_THAN|GREATER_THAN_OR_EQUAL|LESS_THAN_OR_EQUAL|EQUAL|NOT_EQUAL", self.arithmeticExpression)

    def expression(self):
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

    def slices(self):
        at = self.expression()

        if self.currentToken.match("BACK_SLASH"):
            self.advance()

            return [at, self.expression()]

        return [at, at]

    def call(self):
        atom = self.atom()

        stack  = None
        reduce = False
        while self.currentToken.type == "LEFT_BRACKET":
            argNodes = self.getArgs()

            if reduce: stack = CallNode(stack, argNodes)
            else     : stack = CallNode(atom, argNodes); reduce = True

        if self.currentToken.match("LEFT_SLICE"):
            self.advance()

            slices = self.slices()

            if self.currentToken.match("RIGHT_SLICE"):
                self.advance()

                if self.currentToken.match("ASSIGNMENT") and slices[0] == slices[1]:
                    self.advance()

                    return SetNode(atom, slices[0], self.expression())

                return GetNode(atom, slices)
            
            else: raise SyntaxError(f'Unexpected Token: "{self.currentToken.type}", ">>" expected.')

        
        return stack if stack else atom

    def factor(self):
        token = self.currentToken

        if token.type in "ADD|SUB|LENGTH|HEAD|TAIL":
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

            if self.currentToken.match("ASSIGNMENT"):
                self.advance()

                return VariableNode(token.value, self.expression())

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

        elif token.match("TERNARY"):
            self.advance()
            return self.ternaryExpression()

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