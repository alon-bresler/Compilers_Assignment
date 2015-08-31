# Compiler Assignment 1 - parse_ula.py
# CSC3003S
# 14/09/2015
__author__ = 'Alon Bresler'

import ply.yacc as yacc

# Get the token map from the lexer (lex_ula). #
from lex_ula import tokens

# Setting precedence and associativity #
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Constructing a abstract syntax tree #
def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = ('AssignStatement', p[1], p[2], p[3])

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    if (p[2] == '@'):
        p[0] = ('AddExpression',p[2],p[1],p[3])
    elif (p[2] == '$'):
        p[0] = ('SubExpression',p[2],p[1],p[3])
    elif (p[2] == '#'):
        p[0] = ('MulExpression',p[2],p[1],p[3])
    elif (p[2] == '&'):
        p[0] = ('DivExpression',p[2],p[1],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_number(p):
    'expression : FLOAT_LITERAL'
    p[0] = ('FloatExpression',p[1])

# def p_assign(p):
#     '''assignm : ID EQUALS expression'''
#
# def p_expression(p):
#     '''expression : expression PLUS term
#                   | expression MINUS term
#                   | term'''
#
# def p_term(p):
#     '''term : term TIMES factor
#             | term DIVIDE factor
#             | factor'''
#
# def p_facto(p):
#     '''factor : FLOAT_LITERAL'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

result = parser.parse('this1=1')
print (result)

#def readFromFile(file):
#    f = open(file, 'r')
#    data = ""
#    for line in f:
#        data = data + line

#    lexer.input(data)