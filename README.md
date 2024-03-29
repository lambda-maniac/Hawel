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
            - [if-clause](#if-clause)
            - [else-clause](#else-clause)
            - [elif-clause](#elif-clause)
        - [Case statement](#case-statement)
    - [Loops](#loops)
        - [For loop](#for-loop)
        - [While loop](#while-loop)
        - [For-each loop](#for-each-loop)
        - [Loops control flow](#loops-control-flow)
            - [Break](#break-command)
            - [Continue](#continue-command)
    - [Functions](#functions)
        - [Definitions](#definitions)
        - [Simple examples](#simple-examples)
        - [True Haweler example](#true-haweler-example)
    - [Tokens](#tokens)
        - [Block](#block)
        - [Next](#next)
        - [Assignment](#assignment)
        - [Comment](#comment)
        - [If](#if)
        - [Elif](#elif)
        - [Else](#else)
        - [Case](#case)
        - [Switch](#switch)
        - [For](#for)
        - [To](#to)
        - [Of](#of)
        - [By](#by)
        - [While](#while)
        - [Break](#break)
        - [Continue](#continue)
        - [Function](#function)
        - [Return](#return)

# Introduction
This part is the introduction to the Hawel language, it covers from a simple "Hello World!", to things such as variables, types, getting input and arithmetic.

---

Contents:

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

---

Contents:

- [If statement](#if-statement)
    - [if-clause](#if-clause)
    - [else-clause](#else-clause)
    - [elif-clause](#elif-clause)
- [Case statement](#case-statement)

## If statement
This is how we state an if expression:
```
| if <condition> then
    | code...
end
```
The `<condition>` part from the code above represents any expression that could evaluate to a boolean (`1` or `0`, also their variable equivalents: `true` or `false`).

##### If-clause
Here's a simple program to only greet a specific name:
```
| name: get ["Enter your name: "]
| if name == "John Doe" then
    | echo ["welcome!"]
end
```
##### Else-clause
Again, but this time using the `else` clause:
```
| name: get ["Enter your name: "]
| if name == "John Doe" then
    | echo ["welcome!"]
else
    | echo ["Unknown user!"]
end
```
##### Elif-clause
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
The `<condition>` part from the code above represents any expression that could evaluate to a boolean (`1` or `0`, also their variable equivalents: `true` or `false`). Both `<value>` parts can be any kind of value, that is evaluated and returned by the case statement.

Here's a simple use of the case statement:
```
| whatsUp: case 1 ~= 0 select "Math works!" otherwise "Something seems wrong..."
| echo [whatsUp]
```
**Explanation:**

The variable `whatsUp` is going to be assigned `"Math works!"` case the condition `1 ~= 0` is indeed true, otherwise it is assigned `"Something seems wrong..."`. Then it's value is echoed in the second line.

Here you can find the definitions for the [case](#case) token, and the [switch](#switch) token.

###### **This marks the end of [Control flow, booleans and boolean operators](#control-flow-booleans-and-boolean-operators) part.**

# Loops
In this section we will learn how to perform loops of many kinds, such as a simple `for`, a `while`, or even a `for-each`.

- [For loop](#for-loop)
- [While loop](#while-loop)
- [For-each loop](#for-each-loop)
- [Loops control flow](#loops-control-flow)
    - [Break](#break-command)
    - [Continue](#continue-command)

## For loop
For loops in Hawel aren't C-Like loops, they're more like pascal's and lua's, with an initial value, an end value, and a step to increment by.

This is how we would state a for loop without a step in Hawel:
```
| for <variable>: <initialValue> to <endValue> do
    | code...
done
```
And this is how you state with a step value in Hawel:
```
| for <variable>: <initialValue> to <endValue> by <stepValue> do
    | code...
done
```
The `<variable>` part should just be any identifier to be set as our 'iterator', and then be assigned with our `<initialValue>`, so, basically, the first part of the loop is just a [variable declaration](#declaring-variables). After the declaration of our 'iterator', we must state a `<endValue>` for it to reach, and optionally, the `<stepValue>`, which will increment our 'iterator' by it's value each looping. (`<stepValue>` is always 1 if no step is provided, as the first loop example)

Here's some examples on how to loop from 0 to 10 and print each one of those numbers:
###### stepless:
```
| for n: 0 to 11 do </> Needs to be 11, because it always stops at n - 1
    | echo [n]
done
```
###### steping by 2:
```
| for n = 0 to 11 by 2 do
    | echo [n]
done
```
Here you can find the definitions for the [for](#for) token, [to](#to) token, and [by](#by) token.

## While loop
This is how we state a while loop:
```
| while <condition> do
    | code...
done
```

The `<condition>` part from the code above represents any expression that could evaluate to a boolean (`1` or `0`, also their variable equivalents: `true` or `false`).

Here's a simple program that loops through 0 to 10 and prints each one of them:
```
| n = 0
| while n <= 10 do
    | echo [n]
    | n = n + 1
end
```
Here you can find the definitions for the [while](#while) token.

## For-each loop
This is how we state a For-each loop:
```
| for <variable> of <iterable> do
    | code...
done
```
The `<variable>` part should be any identifier, to be set as our 'iterator'. The `<iterable>` part should be any iterable value, such as a list or a string.

Here's an example on how to loop through each letter of a word and print them:
```
| for letter of "I love programming" do
    | echo [letter]
done
```
Could be a list too:
```
| for number of {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} do
    | echo [number]
done
```
Here you can find the definitions for the [for](#for) token and [of](#of) token.

## Loop control flow
This section will teach you how to use the flow control commands `continue` and `break` inside loops.

#### Break command
The break command is used inside loops to stop their looping proccess and jump straight to the end of it's definition.

Here's an example on how to stop the execution of the loop when it reachs the value 5:
```
| for n: 0 to 11 do
    | if n == 5 do 
        | break
    end
    | echo [n]
done
```
The code above will only output:
>0
>1
>2
>3
>4
>5

Reason is; when `n = 5`, the `if` is executed and the break is effectuated, ending the loop routine.

Here you can find the definitions for the [break](#break) token.

#### Continue command
The continue command is used inside loops to stop their current iteration, and jump back to the definition of the loop, to check for it's conditions.

Here's an example on how to skip only the fifth iterarion of a loop:
```
| for n: 0 to 11 do
    | if n == 5 do 
        | continue
    end
    | echo [n]
done
```
The code above will only output:
>0
>1
>2
>3
>4
>6
>7
>8
>9
>10

Reason is; when `n = 5`, the `if` is executed and the continue is effectuated, ending the loop's current iteration and jumping back to the definition.

Here you can find the definitions for the [continue](#continue) token.

###### **This marks the end of the [Loops](#loops) part.**

# Functions
This section will teach us about functions and how to define them.

- [Definitions](#definitions)
- [Simple examples](#simple-examples)
- [True Haweler example](#true-haweler-example)

## Definitions
The standard definition of a function is as it follows:
```
| function <name> [<arguments>] do
    | code...
end
```
The `<name>` part should be any identifier, to take the role as the name of the function. Inside the brackets, you can define either zero or more arguments, all being identifiers too, to be defined inside the function in it's context, when it is called.

Now, you could also define anonymous functions by just omitting it's `<name>`, but writting the world `function` when not giving a name is just painfull, so, use the symbolic version of the token:
```
| @[<arguments>]$ | <<= expression... $
```
Here you can find the definitions for both the [function](#function) token, and the [return](#return) token.

## Simple examples
Function to greet someone:
```
| function greet [name] do
    | echo ["Hello, ", name, "!"]
end
```
Function to calculate the square of a number:
```
| function square [n] do
    | return n * n
end
```
Function to calculate the factorial of a number:
```
| function factorial [n] do
    | n' = 1
    | for i = 1 to n + 1 do
        | n' = n' * i
    done
    | return n'
end
```

## True haweler example
```
| @factorial [n] ::= factorial function
    $
    | <<= :: n == 1
          -- n
          -- n * factorial [n - 1]
$ 
| @map [f] ::= map function
    $
    | <<= (@[list] ::= inner function, so we can curry
        $
        | <<= :: {} == list
              -- {}
              -- f [<$list] <$> map [f] [<*list] ::= Haskell's "f x : map f xs"
    $)
$
| echo [
    map [factorial] [{1, 2, 3, 4, 5}] ::= Curry call to (map factorial) list
]
```
###### **This marks the end of the [Functions](#functions) part.**

---

## Tokens
Collection of all tokens defined in Hawel. (Not all, yet)

##### Block
- `$`
- `do`
- `end`
- `then`
- `done`

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

#### Switch
- `--`
- `select`
- `otherwise`

#### While
- `%`
- `while`

#### For
- `!`
- `for`

#### To
- `=>`
- `to`

#### By
- `..`
- `by`

#### Of
- `;;`
- `of`

#### Break
- `<<<`
- `break`

#### Continue
- `>>>`
- `continue`

#### Function
- `@`
- `def`
- `function`

#### Return
- `<<=`
- `return`

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
