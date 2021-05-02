from _token      import Token
from lexer       import Lexer
from nodes       import *
from _parser     import Parser
from context     import *
from classes     import *
from interpreter import *
from hawelTokens import TOKENS

class Shell:
    def __init__(self):
        self.lineCount = 0
        self.context   = Context('main')

        self.context.symbolTable.symbols = \
        {
            'null': Int(0),
            'pi'  : Int(3.14159265368979),
            'echo': BuiltInPrint(),
            'get' : BuiltInInput(),
            'int' : BuiltInInt(),
            'str' : BuiltInString(),
        }

        self.refreshBuffer()

    def refreshBuffer(self):
        self.line = str(self.lineCount).zfill(3)
        self.in_  = f"[{self.line}] || "
        self.out  = f"({self.line}) :: "
        self.lineCount += 1

    def blockOfCode(self):
        fullCode = ""
        while ((command := input(self.in_)) != "$$$$"):
            fullCode += command
            self.refreshBuffer()
        return fullCode
        
    def run(self):

        while True:

            try:
                command = input(self.in_)
                
                if   command.upper() == "EXIT": break
                elif command         == "$$$$" : command = self.blockOfCode()

                result = Interpreter(Parser(Lexer(TOKENS).lex(command)).parse()).interpretate(self.context).properFormat()
        
                if result == "0": continue

                print(f"{self.out}{result}")
            
            except KeyboardInterrupt: print("")
            except Exception as e   : print(f"{self.out}An Exception has occured ({type(e).__name__}): {e}")
            finally                 : self.refreshBuffer()

if __name__ == '__main__': Shell().run()