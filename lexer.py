from _token import Token

class Lexer:
    import re

    def __init__ (self, tokens):
        self.tokens = tokens

    def lex(self, string):
        self.string  = string
        self.cursor  = 0
        self._cursor = 0
        self.lineno  = 1

        tokenList = []

        while self.cursor < len(self.string):

            tokenFailSafe = 0
            elderCursor   = 0
            tokenBegin    = 0
            tokenEnd      = 0
            _cursor       = 0

            for token, _type in self.tokens.items():
                match = self.re.findall(token, self.string[self.cursor:])

                if match == ['\n']:
                    self.lineno += 1
                    self._cursor = -1

                if match == []: 
                    
                    if (tokenFailSafe := tokenFailSafe + 1) == len(self.tokens):
                        raise SyntaxError (f'Invalid Token: "{self.string[self.cursor]}" at {self.cursor}')
                    
                    continue
            
                tokenBegin   = self._cursor
                
                self.cursor  += len(match[0])
                self._cursor += len(match[0])

                tokenEnd     = self._cursor - 1
            
                if _type == None: continue

                tokenList.append(Token(_type, match[0], tokenBegin, tokenEnd, self.lineno, self.cursor))

        return tokenList