# Compiler Assignment 1 - parse_ula.py
# CSC3003S
# 14/09/2015
__author__ = 'Alon Bresler'

import ply.yacc as yacc
import lex_ula

# Get the token map from the lexer (lex_ula). #
from lex_ula import tokens

programName = ''

# Setting precedence and associativity #
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Constructing a abstract syntax tree #
def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = ('AssignStatement', p[1], p[3])

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    if (p[2] == '@'):
        p[0] = ('AddExpression',p[1],p[3])
    elif (p[2] == '$'):
        p[0] = ('SubExpression',p[1],p[3])
    elif (p[2] == '#'):
        p[0] = ('MulExpression',p[1],p[3])
    elif (p[2] == '&'):
        p[0] = ('DivExpression',p[1],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_number(p):
    'expression : FLOAT_LITERAL'
    p[0] = ('FloatExpression',p[1])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

#result = parser.parse('this1 = 1 @ 2')
#print(result)

# if a result is returned
# if (result != None):
#     print(result)
#
#     if (result[0] == 'AssignStatement'):
#         print(result[0])
#         print('\t' + 'ID,' + result[1])



def processLine(line):
    print(line)

def readFromFile(file):
   prog = file.split('.')
   allData = ""
   f = open(prog[0] + '.tkn', 'r')
   for line in f:
       line = line[0:len(line)-1]
       if (line != "COMMENT" and line != "WHITESPACE"):
            allData = allData+ " "+line
   dataArr = allData.split(' ')

   lineForProcessing = ""
   for i in range (1, len(dataArr)-1):
        if (dataArr[i+1] == '='):
           processLine(lineForProcessing)
           lineForProcessing = dataArr[i]
        else:
            lineForProcessing = lineForProcessing + dataArr[i]





#RUN MAIN
if __name__ == '__main__':
    #programName = sys.argv[1]
    lex_ula.programName = 'ula_samples/numbers.ula'
    lex_ula.readFromFile('ula_samples/numbers.ula')
    readFromFile('ula_samples/numbers.ula')