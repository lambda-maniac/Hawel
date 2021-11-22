# Hawel Esoteric language
This is a basic language I made for **study purposes**. It has almost everything a normal programming language does. In Hawel, we have two types of syntaxes, one which is purely symbolic, and one more verbose. You can use any of them, or even both at the same time. (This document will show you both of them).

Contents of this document:
- [Hawel Esoteric Language](#hawel-esoteric-language)
    - [Introduction](#introduction)
        - [Hello World!](#hello-world)
        - [Declaring variables](#declaring-variables)
        - [Comments](#comments)
    - [Tokens](#tokens)
        - [Next](#next)
        - [Assignment](#assignment)
        - [Comment](#comment)

# Introduction
This part is the introduction to the Hawel language, it covers from a simple "Hello World!", to things such as variables, types, getting input and arithmetic.
- [Hello World!](#hello-world)
- [Declaring variables](#declaring-variables)
- [Comments](#comments)

## Hello World!
Here's a simple "Hello World!" example in Hawel:
```
| echo ["Hello World!"]
```
Breaking apart the code above, we have 5 tokens in total: 
- `| : <NEXT>`
- `echo : <IDENTIFIER>`
- `[ : <OPENING_BRACKET>`
- `"Hello World! : <STRING>` 
- `] : <CLOSING_BRACKET>`

**Explanation:**

First of all, before starting to write an expression in Hawel, you need a `<NEXT>` token, which it's variations can be found here: [next](#next). After that, we see an identifier called `echo`,  which is our 'standard output' function, then we use `[]` to call that function, and pass `"Hello World!"` inside the brackets as it's argument.

## Declaring variables
This is how we can declare variables in Hawel:
```
| name: "John Doe"
| age = 18
| job as "Developer"
| salary is null
```
Breaking apart the first line of the code above, we have 4 tokens in total:
- `| : <NEXT>`
- `name : <IDENTIFIER>`
- `':' : <ASSIGNMENT>` (quotes only for more readability)
- `"John Doe" : <STRING>`

**Explanation:**

As we can see, we have our `<NEXT>` token to indicate a new expression, after that, we have an identifier called `name`, which will be the name of our variable. That name is then proceeded by an `<ASSIGNMENT>` token (in this case, a colon ':', you can find all the definitions here: [assignment](#assignment)), and finally, by the value we want it to be assigned (string `"John Doe"`).

## Comments
This is how we can comment certain parts of our code in Hawel:
```
</> Inline comment.
::= Inline comment.
</ Multiline comment />
[[ Multiline comment ]]
```
The code above is completely ignored by the interpreter. You can see the definition for the comment token here: [comment](#comment)

## Tokens
Collection of all tokens defined in Hawel.

###### Defined at `hawelTokens.py`:
```python
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
```
##### Comment
- `::=`
- `</>`
- `[[ ]]` (Multiline)
- `</ />` (Multiline)

##### Next
- `;`
- `|`
- `endl`
- `thenl`

#### Assignment
- `:`
- `=`
- `as`
- `is`
