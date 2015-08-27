__author__ = 'Alon'

import ply.yacc as yacc

# Get the token map from the lexer (lex_ula). #
from lex_ula import tokens

# Setting precedence and associativity #
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Binary operations for @, $, #, &
# def p_binary_operators(p):
#     '''expression : expression PLUS term
#                   | expression MINUS term
#        term       : term TIMES factor
#                   | term DIVIDE factor'''
#     if p[2] == '@':
#         p[0] = p[1] + p[3]
#     elif p[2] == '$':
#         p[0] = p[1] - p[3]
#     elif p[2] == '#':
#         p[0] = p[1] * p[3]
#     elif p[2] == '&':
#         p[0] = p[1] / p[3]
#
# def p_expression_term(p):
#     'expression : term'
#     p[0] = p[1]
#
# def p_term_factor(p):
#     'term : factor'
#     p[0] = p[1]
#
# def p_factor_num(p):
#     'factor : NUMBER'
#     p[0] = p[1]
#
# def p_factor_expr(p):
#     'factor : LPAREN expression RPAREN'
#     p[0] = p[2]

# Constructing a abstract syntax tree #
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = ('binary-expression',p[2],p[1],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number-expression',p[1])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)