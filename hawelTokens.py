TOKENS = \
{
    # Ignore
    r"^[\s+\n+]": None,

    # Var ~ Not needed anymore?
    #r"^\-\-": "MAKE_VAR",

    # Return
    r"^\<\<\=": "RETURN",
    r"^\>\>\>": "CONTINUE",
    r"^\<\<\<": "BREAK",
    
    # If, Else If, Else
    r"^\?\.\.": "IF",
    r"^\.\?\.": "ELSE_IF",
    r"^\.\.\?": "ELSE",

    # For loop
    r"^\!": "FOR",
    r"^\=\>": "ARROW",
    r"^\.\.": "STEP",

    # Logic 
    r"^\>\=": "GREATER_THAN_OR_EQUAL",
    r"^\<\=": "LESS_THAN_OR_EQUAL",

    r"^\<\<": "LEFT_SLICE",
    r"^\>\>": "RIGHT_SLICE",

    r"^\>": "GREATER_THAN",
    r"^\<": "LESS_THAN",

    r"^\=\=": "EQUAL",
    r"^\~\=": "NOT_EQUAL",

    r"^\~": "NOT",
    r"^\&\&": "AND",
    r"^\|\|": "OR",

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
    r"^[a-zA-Z_\']*[a-zA-Z0-9_\']+": "IDENTIFIER",

    # Symbols #
    r"^\:": "ASSIGNMENT",
    r"^\{": "LEFT_CURLY",
    r"^\}": "RIGHT_CURLY",
    r"^\\": "BACK_SLASH",

    # Arithmetic
    r"^\-": "SUB",
    r"^\+": "ADD",
    r"^\*": "MUL",
    r"^\/": "DIV",
    r"^\^": "POW",
    r"^\(": "LEFT_PARENTHESIS",
    r"^\)": "RIGHT_PARENTHESIS",
}