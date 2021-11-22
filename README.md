# Hawel Esoteric language
This is a basic language I made for **study purposes**. It has almost everything a normal programming language does. In Hawel, we have two types of syntaxes, one which is purely symbolic, and one more verbose. You can use any of them, or even both at the same time. (This document will show you both of them)

[TOC]

## Introduction
This part is the introduction to the Hawel language, it covers from a simple "Hello World!", to things such as variables, types and arithmetic.
### Hello World!
Here's a simple "Hello World!" example in Hawel:
```
| echo ["Hello World!"]
```
Breaking the code above apart, we have 5 tokens in total: 
- `|             : <NEXT>`
- `echo          : <IDENTIFIER>`
- `[             : <OPENING_BRACKET>`
- `"Hello World! : <STRING>` 
- `]             : <CLOSING_BRACKET>`

#### Explanation
First of all, before starting to write an expression in Hawel, you need a `<NEXT>` token, which it's variations can be found here: [tokens](###next)

## Tokens
Collection of all tokens defined in Hawel.
### Next
- `;`
- `|`
- `endl`
- `thenl`

# WIP TESTING
