# Compiler Assignment 1 - parse_ula.py
# CSC3003S
# 14/09/2015
__author__ = 'Alon Bresler'

import ply.yacc as yacc
import lex_ula
import sys

# Get the token map from the lexer (lex_ula). #
from lex_ula import tokens

# Keeping track of errors
isError = False
errorMessage = ""
count = 0

programName = ''
finalString = "Start\n\tProgram"
tabArr = ["\t", "\t", "\t"]

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

def p_id_expression(p):
    'expression : ID'
    p[0] = ('IdentifierExpression',p[1])

# Error rule for syntax errors
def p_error(p):
    global isError
    isError = True
    global errorMessage
    errorMessage = "parse error on line " + str(count)

# Build the parser
parser = yacc.yacc()

# Goes through the array of tabs and returns a string of tabs
def genTabString():
    tabs = ''
    for t in tabArr:
        tabs +=t
    return tabs

# Write the AST to file
def writeToFile():
    words = programName.split('.')
    f = open(words[0] + ".ast", 'w')
    f.write(finalString)
    f.close()

# recursive go through the tree (results array) until the leaves (FLOAT_LITERALS)
def recursiveFormat(result):
    if (len(result) == 2): #If it is a variable or number
        global finalString
        finalString += "\n" + genTabString() + str(result[0])
        tabArr.append('\t')
        #FLOAT_LITERAL
        if (str(result[0]) == 'FloatExpression'):
            finalString += "\n" + genTabString() + "FLOAT_LITERAL," + str(result[1])
        #IDENTIFIER
        elif (str(result[0]) == 'IdentifierExpression'):
            finalString += "\n" + genTabString() + "ID," + str(result[1])
    else:
        finalString += "\n" + genTabString() + str(result[0])
        tabArr.append('\t')
        for i in range (1, len(result)):
            if (str(result[i][0]) != 'group-expression'):
                recursiveFormat(result[i])
                tabArr.remove(tabArr[len(tabArr)-1])
            else:
                recursiveFormat(result[i][1])
                tabArr.remove(tabArr[len(tabArr)-1])

# The beginning of formatting and printing out the tree
# lines always start with an assignment and an ID
def formatResult(result):
    global finalString
    finalString += "\n\t\t"+ str(result[0]) + "\n\t\t\tID," + str(result[1])
    recursiveFormat(result[2]) #recursively do the rest of the tree

# Start processing a line of code
# Send it to the parser and print out AST in correct format
def processLine(line):
    if (line != ''):
        global count
        count += 1
        global tabArr
        tabArr = ["\t", "\t", "\t"]
        if isError == False:
            result = parser.parse(line)
            if isError == False:
                formatResult(result)

# Read from file
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
    programName = sys.argv[1]
    lex_ula.programName = sys.argv[1]
    lex_ula.readFromFile(sys.argv[1])
    readFromFile(sys.argv[1])
    writeToFile()