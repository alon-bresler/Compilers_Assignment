__author__ = 'Alon'

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

returnArr = []

# Setting precedence and associativity #
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Constructing a abstract syntax tree #
def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = [p[2], [p[1]], p[3]]

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    if (p[2] == '@'):
        p[0] = [p[2], p[1],p[3]]
    elif (p[2] == '$'):
        p[0] = [p[2], p[1],p[3]]
    elif (p[2] == '#'):
        p[0] = [p[2], p[1],p[3]]
    elif (p[2] == '&'):
        p[0] = [p[2], p[1],p[3]]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = (p[2])

def p_expression_number(p):
    'expression : FLOAT_LITERAL'
    p[0] = ([p[1]])

def p_id_expression(p):
    'expression : ID'
    p[0] = ([p[1]])

# Error rule for syntax errors
def p_error(p):
    global isError
    isError = True
    global errorMessage
    errorMessage = "parse error on line " + str(count)

# Build the parser
parser = yacc.yacc()

# Start processing a line of code
# Send it to the parser and print out AST in correct format
def processLine(line):
    if (line != ''):
        result = parser.parse(line)
        #temp = ['Program']
        #temp.append(result)
        returnArr.append(result)
            #if isError == False:
               # formatResult(result)       ##DONT NEED TO FORMAT RESULT

# Read from file
def readFromFile(file):
   #Read in the token file and put each line into a block of an array
   #ignoring the COMMENT and WHITESPACE lines

   lex_ula.programName = file
   lex_ula.readFromFile(file)

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
   return returnArr

#RUN MAIN
if __name__ == '__main__':
    programName = sys.argv[1]
    lex_ula.programName = sys.argv[1]
    lex_ula.readFromFile(sys.argv[1])
    readFromFile(sys.argv[1])