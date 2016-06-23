---
layout: post
title:  Making A Toy Language
date:   2016-05-29 07:00 +0800
tags: llvm, python, how-to, projects
---

This is something I've wanted to do for a while and now that the uni semester
is coming to a close, hopefully I'll have time to start it. I'm wanting to
design my own mini-programming language both so I can learn more about how
computers and programming languages work under the hood, and because it might
be a fun exercise that actually gives you a useful product at the end.


## Desired Features

Here are some of the features I want to be built into the language, I'll
probably be coming back and changing them as time goes on and the project
develops.


### Language Semantics

* Procedural
* Compiled
* Object Oriented, but more like Python where you can use them if you want, but
    aren't forced to (i.e. Java)
* Classes are implemented mainly as a dictionary (foo.bar would be equivalent
    to  foo['bar'])
* Strongly typed (compiler resists the temptation to guess what you are wanting
    to do, so adding a string and an integer will throw an error)
* Infer type on definition, but can't change the type after that. Typing is 
    done so that you can either tell the compiler the type of a variable when 
    you first define it ("int i = 5"), otherwise the type will be inferred 
    ("i = 5" means that i is an integer). If it can't be inferred confidently
    then throw an error [NOTE: Does this conflict with the previous point?] 
* Must have namespaces
* Should be able to use C libraries
* Garbage Collected
* No direct access to memory (no pointers)


### Syntax

* Syntax similar to python
* NO semicolons or "end" statements!
* Use indenting for scoping and that
* The language syntax should force/encourage the user to write easily readable
    code
* Docstrings might be useful
* Use dunder methods for "internal" methods like how "+" works, allowing people
    to override them as necessary ("5 + 2" might be turned into "5.__add__(2)"
    internally)

### Implementation

* Use LLVM as an IR and for compiling to binaries
* Python used for lexing/parsing the source code into LLVM Intermediate
    Representation form.


### Some Examples

Function Definitions:

    def foo(int a, int b, str msg="blah"):
        """
        This is a string describing the foo function. 
        "msg" has a default value.  
        """
        print(msg)
        return a + b

Looping:

    list[int] some_list = [1, 2, 3, 4]

    for int i in some_list:
        # Do stuff
        print(i*i)

Conditionals:

    int age = 42

    if age <= 5:
        print('young child')
    elif 5 < age <= 18:
        print("student")
    else:
        print('adult')

Class definitions:

    class Cat:
        def __init__(self, str name):
            str self.name = name

        def make_sound(self):
            print(self.name, 'says "meow"')


## General Plan for the Project

Usually, when implementing a programming language, the process is broken down
into a set of fairly well defined steps. Because I'm planning on using LLVM, 
I'll be able to skip quite a few of the more difficult steps and focus more on
the language design and less on how it's implemented.

These are the general steps when compiling source code into machine code:

1. Lexical Analysis - turn source code into a stream of tokens
2. Syntax Analysis - interpret the tokens (i.e. "foo()" is interpreted as a
   function call)
3. Semantic Analysis - this is where you construct your Abstract Syntax Tree
4. Intermediate Representation - turn the AST into LLVM IR
5. Optimizing - should be a no-brainer
6. Code Generation - turn the LLVM IR into actual machine code to be run on
   your machine.

I'll only need to turn the source code into LLVM IR, after that's done then I
can mostly rely on work that people a lot smarter than me have done for
optimizing the code and then turning it into a binary.

Seeing as this post is already kinda long I think I'll stop here. The next post
will be the first step towards implementing the toy language, lexical analysis.
