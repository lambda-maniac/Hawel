TOKENS = \
{
    r"^[\s+\n+]": None,

    r'^\:\:\=.*': None,
    r"^(?s)\[\[.*?\]\]": None,
    r'^\<\/\>.*': None,
    r"^(?s)\<\/.*?\/\>": None,
    
    r"^return": "RETURN",
    r"^continue": "CONTINUE",
    r"^break": "BREAK",

    r"^prepend": "PREPEND",
    r"^append": "APPEND",

    r"^head": "HEAD",
    r"^tail": "TAIL",

    r"^if": "IF",
    r"^elif": "ELSE_IF",
    r"^else": "ELSE",

    r"^case": "TERNARY",
    r"^(select|otherwise)": "SWITCH",

    r"^for": "FOR",
    r"^to": "ARROW",
    r"^of": "OF",
    r"^by": "STEP",

    r"^not": "NOT",
    r"^and": "AND",
    r"^or": "OR",

    r"^(endl|thenl)": "NEXT",

    r"^(while|until)": "WHILE",

    r"^(function|def)": "FUNCTION",
    
    r"^(end|done|do|then)": "BLOCK",
    r"^length": "LENGTH",

    r"^(as|is)": "ASSIGNMENT",

    r"^\<\<\=": "RETURN",
    r"^\>\>\>": "CONTINUE",
    r"^\<\<\<": "BREAK",

    r"^\<\$\>": "PREPEND",
    r"^\<\*\>": "APPEND",

    r"^\<\$": "HEAD",
    r"^\<\*": "TAIL",

    r"^\?\.\.": "IF",
    r"^\.\?\.": "ELSE_IF",
    r"^\.\.\?": "ELSE",

    r"^\:\:": "TERNARY",
    r"^\-\-": "SWITCH",

    r"^\!": "FOR",
    r"^\=\>": "ARROW",
    r"^\;\;": "OF",
    r"^\.\.": "STEP",

    r"^\>\=": "GREATER_THAN_EQUAL",
    r"^\<\=": "LESS_THAN_EQUAL",

    r"^\<\<": "LEFT_SLICE",
    r"^\>\>": "RIGHT_SLICE",

    r"^\>": "GREATER_THAN",
    r"^\<": "LESS_THAN",

    r"^\=\=": "EQUAL",
    r"^\~\=": "NOT_EQUAL",

    r"^\~": "NOT",
    r"^\&\&": "AND",
    r"^\|\|": "OR",

    r"^(\;|\|)": "NEXT",

    r"^\%": "WHILE",

    r"^\@": "FUNCTION",
    r"^\,": "SEPARATOR",
    r"^\[": "LEFT_BRACKET",
    r"^\]": "RIGHT_BRACKET",
    
    r"^\$": "BLOCK",
    r"^\#": "LENGTH",

    r"^\d+": "INT",
    r'^"[^"]*"': "STRING",
    r"^[a-zA-Z_\']*[a-zA-Z0-9_\']+": "IDENTIFIER",

    r"^(\:|\=)": "ASSIGNMENT",
    r"^\{": "LEFT_CURLY",
    r"^\}": "RIGHT_CURLY",
    r"^\\": "BACK_SLASH",

    r"^\-": "SUB",
    r"^\+": "ADD",
    r"^\*": "MUL",
    r"^\/": "DIV",
    r"^\^": "POW",
    r"^\(": "LEFT_PARENTHESIS",
    r"^\)": "RIGHT_PARENTHESIS",
}