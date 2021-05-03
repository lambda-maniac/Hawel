from _token import Token
from nodes  import *

class ParseResult:
    def __init__(self) : self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.where = None

    def register(self, response):
        if response.error: self.error = response.error
        if response.where: self.where = response.where
        if response.value: self.value = response.value
        return self.value

    def proceed(self, value):
        self.value = value
        return self

    def failure(self, error, whereItHappened):
        self.reset()
        self.error = error
        self.where = whereItHappened
        return self

    def shouldReturn(self):
        return self.error != None

    def __repr__(self):
        return f'{self.value}'

class ReconstructError:
    def __init__(self, code, tokens, parseResult):
        self.code   = code
        self.tokens = tokens
        self.result = parseResult
        
    def reconstruct(self):
        begin, end, line, position = self.result.where[0], self.result.where[1], self.result.where[2], self.result.where[3]

        spacing = ' ' * (begin)
        pointTo = '^' * (end - begin + 1) 

        print(f"Error: ({self.result.error}) in line: ({line}, {begin})")
        print(f"{self.code[0:position]}")
        print(f"{spacing}{pointTo}", end = "")
        print(f"{self.code[position:]}")


class Parser:
    def __init__(self, tokens):
        self.tokens       = tokens
        self.tokenIndex   = -1
        self.currentToken = Token("INT", "0", 0, 0, 0, 0)

        self.advance()

    def parse(self):
        return self.statements()

    def advance(self):
        self.tokenIndex += 1

        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]

    def statements(self):
        response = ParseResult()

        statement = response.register(self.statement())
        if response.shouldReturn(): return response

        statements = [statement]
        while self.currentToken.match("NEXT"):
            self.advance()

            statement = response.register(self.statement())
            if response.shouldReturn(): return response

            statements.append(statement)

        return response.proceed(ListNode(statements))

    def statement(self):
        response = ParseResult()

        if self.currentToken.match("RETURN"):
            self.advance()

            expression = response.register(self.expression())
            if response.shouldReturn(): return response

            return response.proceed(ReturnNode(expression))

        if self.currentToken.match("CONTINUE"):
            self.advance()
            return response.proceed(ContinueNode())

        if self.currentToken.match("BREAK"):
            self.advance()
            return response.proceed(BreakNode())

        expression = response.register(self.expression())
        if response.shouldReturn(): return response

        return response.proceed(expression)

    def binOperation(self, leftTokenType, operations, rightTokenType):
        response = ParseResult()

        leftNode = response.register(leftTokenType())
        if response.shouldReturn(): return response

        while self.currentToken.type in operations:
            operationToken = self.currentToken

            self.advance()

            rightNode = response.register(rightTokenType())
            if response.shouldReturn(): return response
            
            leftNode  = BinOpNode(operationToken, leftNode, rightNode)

        return response.proceed(leftNode)

    def listExpression(self):
        response  = ParseResult()

        nodesList = []

        if self.currentToken.match("RIGHT_CURLY"):
            self.advance()

        else:
            expression = response.register(self.expression())
            if response.shouldReturn(): return response

            nodesList.append(expression)

            while self.currentToken.type == "SEPARATOR":
                self.advance()

                expression = response.register(self.expression())
                if response.shouldReturn(): return response

                nodesList.append(expression)

            if self.currentToken.type != "RIGHT_CURLY":
                return response.failure(f'Expected "," or "{"}"}", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()
        
        return response.proceed(ListNode(nodesList))

    def functionExpression(self):
        response = ParseResult()

        if self.currentToken.type == "IDENTIFIER":
            functionName = self.currentToken
            self.advance()

            if not self.currentToken.match("LEFT_BRACKET"):
                return response.failure(f'Expected Token: "[", got Token: "{self.currentToken.type}" ', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        else:
            functionName = Token("IDENTIFIER", "Anonymous", 0, 0)

            if not self.currentToken.match("LEFT_BRACKET"):
                return response.failure(f'Expected IDENTIFIER or "[", got Token: "{self.currentToken.type}" ', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        argNameTokens = []
        if self.currentToken.type == "IDENTIFIER":
            argNameTokens.append(self.currentToken)
            self.advance()

            while self.currentToken.type == "SEPARATOR":
                self.advance()

                if self.currentToken.type != "IDENTIFIER":
                    return response.failure(f'Expected IDENTIFIER, got: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))

                argNameTokens.append(self.currentToken)
                self.advance()

            if not self.currentToken.match("RIGHT_BRACKET"):
                return response.failure(f'Expected "," or "]", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()

        else:
            if not self.currentToken.match("RIGHT_BRACKET"):
                return response.failure(f'Expected IDENTIFIER or "]", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected "$", got: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        body = response.register(self.statements())
        if response.shouldReturn(): return response

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected "$", got: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        return response.proceed(FunctionDefinitionNode(
            functionName,
            argNameTokens,
            body
        ))

    def whileExpression(self):
        response = ParseResult()

        condition = response.register(self.expression())
        if response.shouldReturn(): return response

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}" ', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        body = response.register(self.statements())
        if response.shouldReturn(): return response

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        return response.proceed(WhileNode(condition, body))

    def forExpression(self):
        response = ParseResult()

        if self.currentToken.type != "IDENTIFIER":
            return response.failure(f'Expected IDENTIFIER, got: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        
        variableName = self.currentToken
        self.advance()

        if self.currentToken.type != "ASSIGNMENT":
            if self.currentToken.type != "OF":
                return response.failure(f'Expected Token: ":" or ";;", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()
            
            iterable = response.register(self.expression())
            if response.shouldReturn(): return response

            if not self.currentToken.match("BLOCK"):
                return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()

            body = response.register(self.statements())
            if response.shouldReturn(): return response

            if not self.currentToken.match("BLOCK"):
                return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()

            return response.proceed(ForEachNode(variableName, iterable, body))

        self.advance()

        startValue = response.register(self.expression())
        if response.shouldReturn(): return response

        if self.currentToken.type != "ARROW":
            return response.failure(f'Expected Token: "=>", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        endValue = response.register(self.expression())
        if response.shouldReturn(): return response

        if self.currentToken.match("STEP"):
            self.advance()

            stepValue = response.register(self.expression())
            if response.shouldReturn(): return response

        else: stepValue = IntNode(Token("INT", 1))

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        body = response.register(self.statements())
        if response.shouldReturn(): return response

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        return response.proceed(ForNode(variableName, startValue, endValue, stepValue, body))

    def ternaryExpression(self):
        response = ParseResult()

        condition = response.register(self.expression())
        if response.shouldReturn(): return response

        if not self.currentToken.match("SWITCH"):
            return response.failure(f'Expected Token: "--", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        caseTrue = response.register(self.expression())
        if response.shouldReturn(): return response

        if not self.currentToken.match("SWITCH"):
            return response.failure(f'Expected Token: "--", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        caseFalse = response.register(self.expression())
        if response.shouldReturn(): return response

        return response.proceed(TernaryNode(condition, caseTrue, caseFalse))

    def ifExpression(self):
        response  = ParseResult()

        cases     = []

        condition = response.register(self.expression())
        if response.shouldReturn(): return response

        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        statements = response.register(self.statements())
        if response.shouldReturn(): return response

        cases.append((condition, statements))

        while self.currentToken.match('ELSE_IF'):
            self.advance()

            condition = response.register(self.expression())
            if response.shouldReturn(): return response
            
            if not self.currentToken.match("BLOCK"):
                return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()

            statements = response.register(self.statements())
            if response.shouldReturn(): return response

            cases.append((condition, statements))

        if self.currentToken.match("ELSE"):
            self.advance()

            statements = response.register(self.statements())
            if response.shouldReturn(): return response

            cases.append((IntNode(Token("INT", 1)), statements))
        
        if not self.currentToken.match("BLOCK"):
            return response.failure(f'Expected Token: "$", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
        self.advance()

        return response.proceed(IfNode(cases))

    def arithmeticExpression(self):
        response = ParseResult()
        
        binOperation = response.register(self.binOperation(self.term, "ADD|SUB|PREPEND|APPEND", self.term))
        if response.shouldReturn(): return response

        return response.proceed(binOperation)

    def comparisonExpression(self):
        response = ParseResult()

        if self.currentToken.match("NOT"):
            operation = self.currentToken
            self.advance()

            comparisonExpression = response.register(self.comparisonExpression())
            if response.shouldReturn(): return response

            return response.proceed(UnaryOpNode(operation, comparisonExpression))

        binOperation = response.register(self.binOperation(self.arithmeticExpression, "GREATER_THAN|LESS_THAN|GREATER_THAN_OR_EQUAL|LESS_THAN_OR_EQUAL|EQUAL|NOT_EQUAL", self.arithmeticExpression))
        if response.shouldReturn(): return response

        return response.proceed(binOperation)

    def expression(self):
        response = ParseResult()

        binOperation = response.register(self.binOperation(self.comparisonExpression, "AND|OR", self.comparisonExpression))
        if response.shouldReturn(): return response

        return response.proceed(binOperation)

    def term(self):
        response = ParseResult()

        binOperation = response.register(self.binOperation(self.factor, "MUL|DIV", self.factor))
        if response.shouldReturn(): return response

        return response.proceed(binOperation)

    def power(self):
        response = ParseResult()

        binOperation = response.register(self.binOperation(self.call, "POW", self.factor))
        if response.shouldReturn(): return response

        return response.proceed(binOperation)
    
    def getArgs(self):
        response = ParseResult()

        self.advance()

        argNodes = []
        if self.currentToken.type == "RIGHT_BRACKET":
            self.advance()
        else:
            expression = response.register(self.expression())
            if response.shouldReturn(): return response

            argNodes.append(expression)
            while self.currentToken.type == "SEPARATOR":
                self.advance()

                expression = response.register(self.expression())
                if response.shouldReturn(): return response

                argNodes.append(expression)

            if self.currentToken.type != "RIGHT_BRACKET":
                return response.failure(f'Expected "," or "]", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))
            self.advance()

        return response.proceed(argNodes)

    def slices(self):
        response = ParseResult()

        at = response.register(self.expression())
        if response.shouldReturn(): return response

        if self.currentToken.match("BACK_SLASH"):
            self.advance()

            end = response.register(self.expression())
            if response.shouldReturn(): return response

            return response.proceed([at, end])

        return response.proceed([at, at])

    def call(self):
        response = ParseResult()

        atom = response.register(self.atom())
        if response.shouldReturn(): return response

        stack  = None
        reduce = False
        while self.currentToken.type == "LEFT_BRACKET":

            argNodes = response.register(self.getArgs())
            if response.shouldReturn(): return response

            if reduce: stack = CallNode(stack, argNodes)
            else     : stack = CallNode(atom, argNodes); reduce = True

        if self.currentToken.match("LEFT_SLICE"):
            self.advance()

            slices = response.register(self.slices())
            if response.shouldReturn(): return response

            if self.currentToken.match("RIGHT_SLICE"):
                self.advance()

                if self.currentToken.match("ASSIGNMENT") and slices[0] == slices[1]:
                    self.advance()

                    expression = response.register(self.expression())
                    if response.shouldReturn(): return response

                    return response.proceed(SetNode(atom, slices[0], expression))

                return response.proceed(GetNode(atom, slices))
            
            else: return response.failure(f'Expected ">>", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))

        return response.proceed(stack) if stack else response.proceed(atom)

    def factor(self):
        response = ParseResult()

        token = self.currentToken

        if token.type in "ADD|SUB|LENGTH|HEAD|TAIL":
            self.advance()

            factor = response.register(self.factor())
            if response.shouldReturn(): return response

            return response.proceed(UnaryOpNode(token, factor))

        power = response.register(self.power())
        if response.shouldReturn(): return response

        return response.proceed(power)

    def atom(self):
        response = ParseResult()

        token = self.currentToken

        if token.type == 'INT':
            self.advance()
            return response.proceed(IntNode(token))

        if token.type == 'STRING':
            self.advance()
            return response.proceed(StringNode(token))

        elif token.type == "IDENTIFIER":
            self.advance()

            if self.currentToken.match("ASSIGNMENT"):
                self.advance()

                expression = response.register(self.expression())
                ############################################################################ NEED
                # if response.shouldReturn: return response ### Why is it always returnin? # TO
                ############################################################################ FIX

                return response.proceed(VariableNode(token.value, expression))

            return response.proceed(VariableAccessNode(token))

        elif token.type == 'LEFT_PARENTHESIS':
            self.advance()
            
            expression = response.register(self.expression())
            if response.shouldReturn: return response

            if self.currentToken.type == 'RIGHT_PARENTHESIS':
                self.advance()

                return response.proceed(expression)

            else:
                return response.failure(f'Expected Token: ")", got Token: "{self.currentToken.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))

        elif token.match("LEFT_CURLY"):
            self.advance()

            listExpression = response.register(self.listExpression())
            if response.shouldReturn: return response

            return response.proceed(listExpression)

        elif token.match("TERNARY"):
            self.advance()

            ternaryExpression = response.register(self.ternaryExpression())
            if response.shouldReturn: return response

            return response.proceed(ternaryExpression)

        elif token.match("IF"):
            self.advance()

            ifExpression = response.register(self.ifExpression())
            if response.shouldReturn: return response

            return response.proceed(ifExpression)

        elif token.match("FOR"):
            self.advance()

            forExpression = response.register(self.forExpression())
            if response.shouldReturn: return response

            return response.proceed(forExpression)

        elif token.match("WHILE"):
            self.advance()

            whileExpression = response.register(self.whileExpression())
            if response.shouldReturn: return response

            return response.proceed(whileExpression)

        elif token.match("FUNCTION"):
            self.advance()

            functionExpression = response.register(self.functionExpression())
            if response.shouldReturn: return response

            return response.proceed(functionExpression)

        return response.failure(f'Unexpected Token: "{token.type}"', (self.currentToken.begin, self.currentToken.end, self.currentToken.line, self.currentToken.position))