# Hawel Esoteric language
This is a basic language I made for **study purposes**. It has almost everything a normal programming language does. In Hawel, we have two types of syntaxes, one which is purely symbolic, and one more verbose. You can use any of them, or even both at the same time. (This document will show you both of them).

---
Contents of this document:
- [Hawel Esoteric Language](#hawel-esoteric-language)
    - [Introduction](#introduction)
        - [Hello World!](#hello-world)
        - [Declaring variables](#declaring-variables)
        - [Comments](#comments)
        - [Getting input](#getting-input)
        - [Arithmetic](#arithmetic)
    - [Control flow, booleans and boolean operators](#control-flow-booleans-and-boolean-operators)
        - [If statement](#if-statement)
        - [case-statement](#case-statement)
    - [Tokens](#tokens)
        - [Next](#next)
        - [Assignment](#assignment)
        - [Comment](#comment)
        - [If](#if)
        - [Elif](#elif)
        - [Else](#else)
        - [Case](#case)
        - [Select](#select)

# Introduction
This part is the introduction to the Hawel language, it covers from a simple "Hello World!", to things such as variables, types, getting input and arithmetic.
- [Hello World!](#hello-world)
- [Declaring variables](#declaring-variables)
- [Comments](#comments)
- [Getting input](#getting-input)
- [Arithmetic](#arithmetic)

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

## Getting input
In Hawel, the way of getting user input from the console, is by calling the function `get`. It always returns the input as a string, and also accepts a string as a prompt. 

See now a simple greeting program:
```
| name: get ["Enter your name: "]
| echo ["Hello, ", name, "!"]
```
**Explanation:**

The code above simply assigns the return value of the `get` function, and then echoes `"Hello, "`, the variable `name`, and finally an exclamation point (`"!"`).

## Arithmetic
All four basic arithmetic operators are present in Hawel: `+`,`-`,`*` and`/`.  (We also have `^`, for exponentiation)

See now a simple program performing all of those operations on two numbers:
```
| a = int [get ["Enter a value for 'a': "]] </> Note that here we are using the `int` function,
| b = int [get ["Enter a value for 'b': "]] </> to convert the string returned by `get` to a number.
| add = a + b
| sub = a - b
| mul = a * b
| div = a / b
| pow = a ^ b
| echo [a, " + ", b, " = ", add]
| echo [a, " - ", b, " = ", sub]
| echo [a, " * ", b, " = ", mul]
| echo [a, " / ", b, " = ", div]
| echo [a, " ^ ", b, " = ", pow]
```
**Explanation:**

We start by assigning two numbers (`a` and `b`) the input of the user, but, before that, we pass the return of the `get` function, to another function called `int`, which will convert the string returned to a int, so that we can perform arithmetic operations on them.

After that, we just assign some variables the value of each operation, to then echo each one of them to the console.

###### **This marks the end of the [Introduction](#introduction) part.**

# Control flow, booleans and boolean operators
Here we are going to learn the control flow commands, such as `if` statements and `case` statements. Not only that, but boolean operatos, like `==` (equals), `~` (not), `~=` (not equals), `&&` (and), `||` (or) ,  `>` (greater than), `<` (less than), `>=` (greater or equal) and `<=` (less or equal).

- [If statement](#if-statement)
- [case-statement](#case-statement)

## If statement
This is how we state an if expression:
```
| if <condition> then
    | code...
end
```
The `<condition>` part from the code above represents any expression that could evaluate to a boolean (`1` or `0`, also their variable equivalents: `true` or `false`).

Here's a simple program to only greet a specific name:
```
| name: get ["Enter your name: "]
| if name == "John Doe" then
    | echo ["welcome!"]
end
```
Again, but this time using the `else` clause:
```
| name: get ["Enter your name: "]
| if name == "John Doe" then
    | echo ["welcome!"]
else
    | echo ["Unknown user!"]
end
```
Now, with the `elif` clause:
```
| name: get ["Enter your name: "]
| if name == "John Doe" then
    | echo ["welcome!"]
elif name == "Jane Doe" then
    | echo ["welcome!"]
else
    | echo ["Unknown user!"]
end
```
Same of the above, but simplifying the `elif` with an `||`:
```
| name: get ["Enter your name: "]
| if name == "John Doe" || name == "John Doe" then
    | echo ["welcome!"]
else
    | echo ["Unknown user!"]
end
```
Here you can find all the definitions for the [if](#if) token, [elif](#elif) token, and [else](#else) token.

## Case statement
The case statement of Hawel isn't like a conventional case expression, it's semantically equal to a generic ternary expression.

This is how we state a case expression in Hawel:
```
| case <condition> select <value> otherwise <value>
```
The <condition> part from the code above represents any expression that could evaluate to a boolean (`1` or `0`, also their variable equivalents: `true` or `false`). Both `<value>` parts can be any kind of value, that is evaluated and returned by the case statement.

Here's a simple use of the case statement:
```
| whatsUp: case 1 ~= 0 select "Math works!" otherwise "Something seems wrong..."
| echo [whatsUp]
```
**Explanation:**

The variable `whatsUp` is going to be assigned `"Math works!"` case the condition `1 ~= 0` is indeed true, otherwise it is assigned `"Something seems wrong..."`. Then it's value is echoed in the second line.

Here you can find the definitions for the [case](#case) token, and the [select, otherwise](#select) token.

---

## Tokens
Collection of all tokens defined in Hawel.

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

#### If
- `?..`
- `if`

#### Elif
- `.?.`
- `elif`

#### Else
- `..?`
- `else`

#### Case
- `::`
- `case`

#### Select
- `--`
- `select`
- `otherwise`

---

#### Raw
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
