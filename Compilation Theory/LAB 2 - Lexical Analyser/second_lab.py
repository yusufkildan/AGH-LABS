#!/usr/bin/python

import sys
import ply.lex as lex

# Reserved Keywords: if, else, for, while, zeros, eye, ones, print

reserved = {'if': 'IF', 'else': 'ELSE', 'for': 'FOR',
            'while': 'WHILE', 'zeros': 'ZEROS','eye': 'EYE', 'ones': 'ONES', 'print': 'PRINT', 'break': 'BREAK', 'continue': 'CONTINUE', 'return': 'RETURN'}

# Tokents

tokens = ['PLUS',  'MINUS',  'TIMES',  'DIVIDE', 'ID', 'INTNUM', 'FLOATNUM', 'DOTADD',
          'SUBASSIGN', 'DOTSUB', 'MULASSIGN', 'DOTMUL', 'DIVASSIGN', 'DOTDIV', 'ADDASSIGN', 'EQ', 'GEQ', 'LEQ', 'GREAT', 'LESS', 'NOTEQ'
] + list(reserved.values())

# Literals

literals = ['=', '(', ')', ';', '\'', '[', ']', '{', '}', ',', ':']

# Ignore Comment and Whitespace

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# Integer numbers, Float numbers

def t_FLOATNUM(t):
    r'[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?'
    t.colno = find_column(t.lexer.lexdata,t)
    t.value = float(t.value)
    return t
    
def t_INTNUM(t):
    r'\d+'
    t.colno = find_column(t.lexer.lexdata,t)
    t.value = int(t.value)
    return t

# Binary Operations: +, -, *, /

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'

# Matrix Element-Wise Binary Operations:  .+, .-, .*, ./

def t_DOTADD(t):
    r'\.\+'
    t.colno = find_column(t.lexer.lexdata,t)
    return t

def t_DOTSUB(t):
    r'\.-'
    t.colno = find_column(t.lexer.lexdata,t)
    return t

def t_DOTMUL(t):
    r'\.\*'
    t.colno = find_column(t.lexer.lexdata,t)
    return t

def t_DOTDIV(t):
    r'\./'
    t.colno = find_column(t.lexer.lexdata,t)
    return t

# Assignment Operations: =, +=, -=, *=, /=

def t_ASSIGN(t):
    r'\='
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = '='
    return t

def t_ADDASSIGN(t):
    r'\+='
    t.colno = find_column(t.lexer.lexdata,t)
    return t

def t_SUBASSIGN(t):
    r'-='
    t.colno = find_column(t.lexer.lexdata,t)
    return t

def t_MULASSIGN(t):
    r'\*='
    t.colno = find_column(t.lexer.lexdata,t)
    return t

def t_DIVASSIGN(t):
    r'/='
    t.colno = find_column(t.lexer.lexdata,t)
    return t

# Parantheses: (,), [,], {,}

def t_LPAREN(t):
    r'\('
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = '('
    return t

def t_RPAREN(t):
    r'\)'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = ')'
    return t

def t_LBRACKET(t):
    r'\['
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = '['
    return t

def t_RBRACKET(t):
    r'\]'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = ']'
    return t

def t_LBRACE(t):
    r'\{'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = '{'
    return t

def t_RBRACE(t):
    r'\}'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = '}'
    return t

# Matrix Transpose: '

def t_TRANSPOSE(t):
    r'\''
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = '\''
    return t

# Comma and Semicolon: ;,

def t_SEMICOLON(t):
    r';'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = ';'
    return t

def t_COMMA(t):
    r','
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = ','
    return t

# Identifiers

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Range Selection: :

def t_RANGE(t):
    r':'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = ':'
    return t

# Relational Operations: <, >, <=, >=, !=, ==

def t_EQ(t):
    r'!='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_NOTEQ(t):
    r'=='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_GEQ(t):
    r'>='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_LEQ(t):
    r'<='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_GREAT(t):
    r'>'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_LESS(t):
    r'<'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

# Line No, Column No

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# Error

def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

lexer = lex.lex()
try:
    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    file = open(filename, "r");
    lexer.input( file.read() )
    for token in lexer:
        print("(%d, %d): %s(%s)" %(token.lineno, token.colno, token.type, token.value))
except:
    print("Cannot open file %s\n", filename)
