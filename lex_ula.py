# Compiler Assignment 1 - lex_ula.py
# CSC3003S
# 14/09/2015
__author__ = 'Alon Bresler'

import ply.lex as lex

# List of token names #
tokens = ('FLOAT_LITERAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN', 'ID', 'COMMENT', 'WHITESPACE')

# Regular expression rules for tokens #
t_PLUS      =   r'\@'
t_MINUS     =   r'\$'
t_TIMES     =   r'\#'
t_DIVIDE    =   r'\&'
t_EQUALS    =   r'\='
t_LPAREN    =   r'\('
t_RPAREN    =   r'\)'

# Regular expression for ID #
def t_ID(t):
    r'[_a-zA-Z][a-zA-Z0-9]*'
    return t
# Regular expression for WHITESPACE
def t_WHITESPACE(t):
    r'\s+'
    return t

# Regular expression for COMMENT
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/) |(//.*)'
    return t

# A regular expression rule with some action code #
def t_FLOAT_LITERAL(t):
    r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
    return t

# Define a rule so we can track line numbers #
#def t_newline(t):
 #   r'\n+'
  #  t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs) #
#t_ignore  = ' \t'

# Error handling rule #
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer #
lexer = lex.lex()

#####################
# TOKENIZE AND PRINT#
#####################
def tokenize():
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        #print(tok)
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)

        # Printing out arithmetic symbols
        if tok.type == 'PLUS':
            print('@')
        elif tok.type == 'MINUS':
            print('$')
        elif tok.type == 'TIMES':
            print('#')
        elif tok.type == 'DIVIDE':
            print('&')
        # Printint parens
        elif tok.type == 'LPAREN':
            print('(')
        elif tok.type == 'RPAREN':
            print(')')
        # How to print out IDs and FLOAT_LITERALS
        elif tok.type == 'ID' or tok.type == 'FLOAT_LITERAL':
            print(tok.type + "," + str(tok.value))
        # Just print equal sign
        elif tok.type == 'EQUALS':
            print('=')
        # Print out whitespace
        elif tok.type == 'WHITESPACE':
            print('WHITESPACE')
        #Print out when COMMENT
        elif tok.type == "COMMENT":
            print(tok.type)


#######################
# READ DATA FROM FILE #
#######################
def readFromFile(file):
    f = open(file, 'r')
    data = ""
    for line in f:
        data = data + line

    lexer.input(data)
    tokenize()

#RUN MAIN
if __name__ == '__main__':
    readFromFile('ula_samples/comments.ula')

