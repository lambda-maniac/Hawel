# Hawel Esoteric language
This is a basic language I made for **study purposes**. It has almost everything a normal programming language does. (Well, I think...)

## Syntax
In Hawel, we have two types of syntaxes, one which is purely symbolic, and one more verbose. You can use both of them at the same time if you want.

#### Per example, you can declare a function these ways:
```
function foo [params] do 
    statements 
end;
```
Remembering that code blocks can be envolved by any type of delimiter, such as ```do```, ```then```, ```end``` or ```done```. So basically, you could have 
atrocities like:
```
function foo [params] end
    statements
then;
```
Following now, a more symbolic declaration:
```
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
```
integer: 10 |

string: "Text" |

list: {1, 2, 3, 4, 5} |
```
Verbose:
```
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
```
list: {1, 2, 3, 4, 5} |
    this could be a String too.

<$list|
    out: 1

<*list|
    out: {2, 3, 4, 5}

#list|
    out: 5

list<<0>> : 0 |
    list is now {0, 2, 3, 4, 5}

list<<2\4>> |
    out: {2, 3}

```
Verbose:
```
list: {1, 2, 3, 4, 5};
    this could be a String too.

head list;
    out: 1

tail list;
    out: {2, 3, 4, 5}

length list;
    out: 5

list<<0>> is 0;
    list is now {0, 2, 3, 4, 5}

list<<2\4>>;
    out: {2, 3}

```
### Note:
Although Hawel seems to only have support for ```int``` type, it has for ```float``` too. I was just too lazy to make it parse floats, so, if somehow you really need floats, you can get it by implementing a function like:
```
@float [n] $ <<= n / 1 $;
```
if you didn't understand what's above, here's a more "readable" version:
```
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
```
option: int [get ["Enter a option between 1 and 2 : "]];

?.. option == 1 $
    echo ["You selected option 1."]
.?. option == 2 $
    echo ["You selected option 2."]
..? echo ["You selected another option."] $|
```
Verbose:
```
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
```
status: :: 1 == 1
        -- "Math Works, lel."
        -- "Wtf?"|
```
Verbose
```
status: case 1 == 1
        select "Math Works, lel."
        select "Wtf?";
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
```
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
```
for number: 0 to 10 do 
    echo [number] 
done;

for number: 0 to 10 by 2 do
    echo [number]
done;

for number of {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} do 
    echo [number] 
done;

number: 0;
while number <= 10 do
    echo [number]; 
    number: number + 1 
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
```
@add [a, b] $
    <<== a + b
$|
```
Verbose:
```
function add [a, b] do
    return a + b
end;
```
# That's all of the basics! Now you can torture yourself by trying the language!
## Here are some more complex examples:
### Factorial function - Hawel program:
```
'program': "Factorial Example .hw"
| @factorial[n]
    $ <<= :: n == 1
          -- n
          -- n * factorial [n - 1]
$
| n: int [get ["Enter a number: "]]
| echo ["Factorial of", n, "is", factorial[n]]

```
### Map function (loop) - Hawel program:
```
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
### Map function (append-loop) - Hawel program:
```
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
### Map function (recursive-currying) - Hawel program:
```
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