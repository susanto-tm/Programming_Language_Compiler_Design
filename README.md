# Programming Language Compiler Design
This project takes insipiration from Python, Haskell, and MATLAB to create an interpreter for a toy programming language. The language supports most basic modern programming language features including functions, loops, conditional statements, dynamic variable assignment, runtime library, and basic implementations of recursion and some backtracking.

## Prerequisites

Before running the file, make sure to have `SymPy` installed and `Python` in order to run the sample code successfully.

## Testing Sample Code
The file `run.py` has the following flags defined in order to see the process or run the sample code file, labeled `sample_code.ma`:

1. `--file` is to use a user defined file (optional)
2. `--lexer` is to view lexer streams as the lexing process is running
3. `--run` is to run the parser and evaluate the sample code if a file is not provided.

## Files

### Lexer

The lexer is defined in `Lexer.py` and holds definitions of reserved tokens and keywords using regular expressions. It uses the `lex` module in the PLY library.


### Parser

The parser is defined in `Parser.py` and holds syntax definition using the Backus-Naur form (BNF) that will be evaluated by the `yacc` module in the PLY library. Each definition in the parser is used together with class defined nodes that will build the abstract syntax tree (AST) while syntax parsing.

### Math Functions

The library of math functions is defined in `math_functions.py` and holds definitions for the built-in math functions.

### Abstract Syntax Tree

The AST class is defined in `AST.py` and has two main sections: code interpretation and processing and AST nodes. The former is implemented based on the class name of each node and recursively does a postorder traversal to visit each node until the tree is evaluated.

## Current Features

### Supported Features

1. Functions (simple implementations of functions)
2. Lists with indexing and slicing similar to Numpy
3. Dynamically typed variables
4. For and While Loops
5. Conditional statements including if and else statements and switch case statements
6. Built-in functions
	1. Mathematical functions: integration, differentiation, trigonometric functions, Maximum and Minimum (accepts any data type)
	
For a more descriptive syntax and guideline on how the language is structured see the [sample code](https://github.com/susanto-tm/Programming_Language_Compiler_Design/blob/master/sample_code.ma).

