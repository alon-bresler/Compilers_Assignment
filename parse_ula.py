# Compiler Assignment 1 - parse_ula.py
# CSC3003S
# 14/09/2015
__author__ = 'Alon Bresler'

import ply.yacc as yacc
import lex_ula
import sys

# Get the token map from the lexer (lex_ula). #
from lex_ula import tokens

programName = ''
finalString = "Start\n\tProgram\n\t\t"

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

def writeToFile():
    words = programName.split('.')
    f = open(words[0] + ".ast", 'w')
    f.write(finalString)
    f.close()

def recursiveFormat(result):
    if (len(result) == 2):
        global finalString
        finalString += "\n\t\t\t\t" + result[0] + "\n\t\t\t\t\tFLOAT_LITERAL," + result[1]
    else:
        finalString += "\n\t\t\t" + result[0]
        for i in range (1, len(result)):
            recursiveFormat(result[i])


def formatResult(result):
    #print("Start")
    #print("\tProgram")

    #print("\t\t" + result[0])
    #print("\t\t\tID," + result[1])
    global finalString
    finalString += result[0] + "\n\t\t\tID," + result[1]

    recursiveFormat(result[2])
    print(finalString)



def processLine(line):
    if (line != ''):
        result = parser.parse(line)
        formatResult(result)


def readFromFile(file):

   #Read in the token file and put each line into a block of an array
   #ignoring the COMMENT and WHITESPACE lines
   prog = file.split('.')
   allData = ""
   f = open(prog[0] + '.tkn', 'r')
   for line in f:
       line = line[0:len(line)-1]
       if (line != "COMMENT" and line != "WHITESPACE"):
            allData = allData+ " "+line
   dataArr = allData.split(' ')

    #Remove the identifiers ID and FLOAT_LITERAL
   for i in range (1, len(dataArr)):
        if (dataArr[i][0:2] == 'ID' or dataArr[i][0:13] == 'FLOAT_LITERAL'):
            s = dataArr[i].split(',')
            dataArr[i] = s[1]


    #Go through the array and split up the array into input lines.
   #Each line starts with an ID and an EQUALS
   lineForProcessing = ""
   for i in range (1, len(dataArr)-1):
        if (dataArr[i+1] == '='):
           processLine(lineForProcessing)
           lineForProcessing = dataArr[i]
        else:
            lineForProcessing = lineForProcessing + dataArr[i]
   processLine(lineForProcessing + dataArr[len(dataArr)-1])





#RUN MAIN
if __name__ == '__main__':
    programName = 'myExamples/basicAssignment.ula'
    lex_ula.programName = 'myExamples/basicAssignment.ula'
    lex_ula.readFromFile('myExamples/basicAssignment.ula')
    readFromFile('myExamples/basicAssignment.ula')

    #programName = sys.argv[1]
    #lex_ula.programName = sys.argv[1]
    #lex_ula.readFromFile(sys.argv[1])
    #readFromFile(sys.argv[1])

    writeToFile()