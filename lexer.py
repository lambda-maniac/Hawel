from token import Token

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
