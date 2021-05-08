# Hawel Esoteric language
This is a basic language I made for **study purposes**. It has almost everything a normal programming language does. (Well, I think...)

## Syntax
In Hawel, we have two types of syntaxes, one which is purely symbolic, and one more verbose. You can use both of them at the same time if you want.

#### Per example, you can declare a function these ways:
```vb
function foo [params] do 
    statements 
end;
```
Remembering that code blocks can be envolved by any type of delimiter, such as ```do```, ```then```, ```end``` or ```done```. So basically, you could have 
atrocities like:
```vb
function foo [params] end
    statements
then;
```
Following now, a more symbolic declaration:
```cs
@foo [params] $
    statements
$|
```
Yes, the pipe symbol ends a statement... Why do you even care?

## Commands and Basics
Here we have some examples on how to use the language:

## Variables and types:
* ```<ASSIGNMENT>```'s can be substituted by either ```:``` or (```=```, ```as```, ```is```).
```
identifier <ASSIGNMENT> value <ENDL>
```
### Examples:
Symbolic:
```cs
integer: 10 |

string: "Text" |

list: {1, 2, 3, 4, 5} |
```
Verbose:
```vb
integer = 10;

string as "Text";

list is {1, 2, 3, 4, 5};
```
## Some 'list/string unique' operators:
* ```<ASSIGNMENT>```'s can be substituted by either ```:``` or (```=```, ```as```, ```is```).
* ```<HEAD>```'s can be substituted by either ```<$``` or ```head```.
* ```<TAIL>```'s can be substituted by either ```<*``` or ```tail```.
* ```<LENGTH>```'s can be substituted by either ```#``` or ```length```.
* ```<PREPEND>```'s can be substituted by either ```<$>``` or ```prepend```.
* ```<APPEND>```'s can be substituted by either ```<*>``` or ```append```.
* ```<SLICE>```'s can be substituted by either ```<<index>>``` or ```<<begin\end>>```.
* ```<ENDL>```'s can be substituted by either ```|``` or ```;```.
### Head:
```
<HEAD> list <ENDL>
```
### Tail:
```
<TAIL> list <ENDL>
```
### Length:
```
<LENGTH> list <ENDL>
```
### Slicing:
```
list <SLICE>(begin\end) <ENDL>
```
### Changing an item of a list:
```
list <SLICE> <ASSIGNMENT> value <ENDL>
```
### Prepending:
```
value <PREPEND> list <ENDL>
```
### Appending:
```
list <APPEND> value <ENDL>
```
### Examples:
Symbolic:
```cs
list: {1, 2, 3, 4, 5} |
    this could be a String too.

<$list|
    out: 1

<*list|
    out: {2, 3, 4, 5}

0 <$> list|
    out: {0, 1, 2, 3, 4, 5}

list <*> 6|
    list is now {1, 2, 3, 4, 5, 6}

#list|
    out: 5

list<<0>> : 0 |
    list is now {0, 2, 3, 4, 5}

list<<2\4>> |
    out: {2, 3}

```
Verbose:
```vb
list as {1, 2, 3, 4, 5};
    this could be a String too.

head list;
    out: 1

tail list;
    out: {2, 3, 4, 5}

0 prepend list;
    out: {0, 1, 2, 3, 4, 5}

list append 6;
    list is now {1, 2, 3, 4, 5, 6}

length list;
    out: 5

list<<0>> is 0;
    list is now {0, 2, 3, 4, 5}

list<<2\4>>;
    out: {2, 3}

```
### Note:
Although Hawel seems to only have support for ```int``` type, it has for ```float``` too. I was just too lazy to make it parse floats, so, if somehow you really need floats, you can get it by implementing a function like:
```cs
@float [n] $ <<= n / 1 $;
```
if you didn't understand what's above, here's a more "readable" version:
```vb
function float [n] do
    return n / 1
end;
```
**It's a feature, stfu.**
## If statements:
* ```<IF>```'s can be substituted by either ```?..``` or ```if```.
* ```<ELIF>```'s can be substituted by either ```.?.``` or ```elif```.
* ```<ELSE>```'s can be substituted by either ```..?``` or ```else```.
* ```<BLOCK>```'s can be substituted by either ```$``` or (```do```, ```done```, ```then```, ```end```).
* ```<ENDL>```'s can be substituted by either ```|``` or ```;```.
### If Statement:
```
<IF> condition <BLOCK> statements <BLOCK><ENDL>
```
### If-Else statement:
```
<IF> condition <BLOCK> statements <ELSE> statements <BLOCK><ENDL>
```

### If-Elif-Else statement:
```
<IF> condition <BLOCK> statements <ELIF> condition <BLOCK> statements <ELSE> statements <BLOCK><ENDL>
```
### Example:
Symbolic:
```cs
option: int [get ["Enter a option between 1 and 2 : "]];

?.. option == 1 $
    echo ["You selected option 1."]
.?. option == 2 $
    echo ["You selected option 2."]
..? echo ["You selected another option."] $|
```
Verbose:
```vb
option: int[get ["Enter a option between 1 and 2 : "]];

if option == 1 then
    echo ["You selected option 1."]
elif option == 2 then
    echo ["You selected option 2."]
else 
    echo ["You selected another option."]
end;
```
## Ternary statements:
* ```<TERNARY>```'s can be substituted by either ```::``` or ```case```.
* ```<CASE>```'s can be substituted by either ```--``` or ```select```.
* ```<ENDL>```'s can be substituted by either ```|``` or ```;```.
```
<TERNARY> condition <CASE> true <CASE> false <ENDL>
```
### Examples:
Symbolic:
```cs
status: :: 1 == 1
        -- "Math Works, lel."
        -- "Wtf?"|
```
Verbose
```vb
status: case 1 == 1
        select "Math Works, lel."
        otherwise "Wtf?";
```
## Loop statements:
* ```<FOR>```'s can be substituted by either ```!``` or ```for```.
* ```<TO>```'s can be substituted by either ```=>``` or ```to```.
* ```<BY>```'s can be substituted by either ```..``` or ```by```.
* ```<OF>```'s can be substituted by either ```;;``` or ```of```.
* ```<WHILE>```'s can be substituted by either ```%``` or ```while```.
* ```<BLOCK>```'s can be substituted by either ```$``` or (```do```, ```done```, ```then```, ```end```).
* ```<ENDL>```'s can be substituted by either ```|``` or ```;```.

### Simple for:
```
<FOR> variable <ASSIGNMENT> begin <TO> end (<BY> step)? <BLOCK> statements <BLOCK><ENDL>
```
### Simple for each:
```
<FOR> variable <OF> iterable <BLOCK> statements <BLOCK><ENDL>
```
### Simple while:
```
<WHILE> condition <BLOCK> statements <BLOCK><ENDL>
```
### Examples:
Symbolic:
```cs
! number: 0 => 10 $ echo [number] $|

! number: 0 => 10 .. 2 $ echo [number] $|

! number ;; {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} $ echo [number] $|

number: 0;
% number <= 10 $ 
    echo [number]; 
    number: number + 1 
$|
```
verbose:
```vb
for number as 0 to 10 do 
    echo [number] 
done;

for number as 0 to 10 by 2 do
    echo [number]
done;

for number of {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} do 
    echo [number] 
done;

number as 0;
while number <= 10 do
    echo [number]; 
    number is number + 1 
done;
```
## Functions
* ```<FUNCTION>```'s can be substituted by either ```@``` or (```def```, ```function```).
* ```<RETURN>```'s can be substituted by either ```<<=``` or ```return```.
* ```<BLOCK>```'s can be substituted by either ```$``` or (```do```, ```done```, ```then```, ```end```).
* ```<ENDL>```'s can be substituted by either ```|``` or ```;```.
### Simple definition:
```
<FUNCTION> identifier [parameters] <BLOCK> statements <BLOCK><ENDL>
```
### Anonymous definition:
```
<FUNCTION> [parameters] <BLOCK> statements <BLOCK><ENDL>
```
### Examples:
Symbolic:
```cs
@add [a, b] $
    <<== a + b
$|
```
Verbose:
```vb
function add [a, b] do
    return a + b
end;
```
# That's all of the basics! Now you can torture yourself by trying the language!
## Here are some more complex examples:
### Factorial function - Hawel program:
```cs
'program': "Factorial Example .hw"
| @factorial[n]
    $ <<= :: n == 1
          -- n
          -- n * factorial [n - 1]
$
| n: int [get ["Enter a number: "]]
| echo ["Factorial of", n, "is", factorial[n]]

```
### Factorial function (verbose syntax) - Hawel program:
```vb
'program': "Factorial Example .Hw (Verbose Syntax)";
function factorial[n] do
    return case n == 1
           select n
           otherwise n * factorial[n - 1]
end;
n: int [get ["Enter a number: "]];
echo ["Factorial of", n, "is", factorial[n]]

```
### Map function (loop) - Hawel program:
```cs
'prgram': "Map Example (loop) .hw"
| @map [f; list]
    $ ! n: 0 => #list
        $ list<<n>> : f [list<<n>>]
    $
    | <<= list
$
| @main[]
    $ list: {1, 2, 3, 4, 5}
    | square: (@[n]$ <<= n * n $)
    | echo [map [square; list]]
$
| main[]
```
### Map function (loop, verbose syntax) - Hawel program:
```vb
'prgram': "Map Example (loop, verbose syntax) .hw"
function map [f, list] do
    for n as null to length list do
        list<<n>> is f [list<<n>>]
    done;
    return list
end;

function main [] do
    list as {1, 2, 3, 4, 5};
    square as (function[n] do return n * n end);
    echo [map [square, list]]
end; main[]
```
### Map function (append-loop) - Hawel program:
```cs
'program': "Map Example (append-loop) .hw"
| @map [f; list]
    $ list' : {}
    | ! n: 0 => #list
        $ list' <*> f [list<<n>>]
    $
    | <<= list'
$
| @main[]
    $ list: {1, 2, 3, 4, 5}
    | square: (@[n]$ <<= n * n $)
    | echo [map [square; list]]
$
| main[]
```
### Map function (append-loop, verbose syntax) - Hawel program:
```vb
'program': "Map Example (append-loop, verbose syntax) .hw";
function map [f, list] do
    list' as {};
    for element of list do
        list' append f [element]
    done;
    return list'
end;

function main [] do
    list as {1, 2, 3, 4, 5};
    square as (function[n] do return n * n end);
    echo [map [square, list]]
end; main[]
```
### Map function (recursive-currying) - Hawel program:
```cs
'program': "Map Example (recursive-currying) .hw"
| (@map [f]
    $ <<= (@[list]
        $ <<= :: <$list == {}
              -- {}
              -- f [<$list] <$> map [f] [<*list] 
    $)
$)
| @main[]
    $ numbers: {1, 2, 3, 4, 5}
    | square: (@[n]$ <<= n * n $)
    | echo [map [square] [numbers]]
$
| main[]
```
### Map function (recursive-currying, verbose syntax) - Hawel program:
```vb
'program': "Map Example (recursive-currying, verbose syntax) .hw";
function map [f] do
    return (function [list] do
                return case head list == {}
                       select {}
                       otherwise f [(head list)] prepend map [f] [(tail list)]
            end)
end;

function main[] do
    numbers: {1, 2, 3, 4, 5};
    squareN: (function[n] do return n * n end);

    echo [map [squareN][numbers]]

end; main[]

```