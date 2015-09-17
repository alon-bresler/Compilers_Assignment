__author__ = 'Alon'

import sys
import lex_ula
import parse_ula

fileName = 'ula_error_samples/testError.ula'

# array to hold instantiated variable names
varArray = []

#######################
# READ DATA FROM FILE #
#######################
def readFromFile(file):
    f = open(file, 'r')
    data = ""
    for line in f:
        data = data + line

######################################
# RUN THE ULA CODE THROUGH THE LEXER #
######################################
def runLexer(file):
    lex_ula.programName = file
    lex_ula.readFromFile(file)

    #write to file if there is an error
    if lex_ula.isError:
        print(lex_ula.errorMessage)
        writeToErrorFile(lex_ula.errorMessage)
    #do the parser if there was no error in the lexer
    else:
        runParser(file)

#######################################
# RUN THE ULA CODE THROUGH THE PARSER #
#######################################
def runParser(file):
    parse_ula.programName = file
    parse_ula.readFromFile(file)

    #write to file if there is a parser error
    if parse_ula.isError:
        print(parse_ula.errorMessage)
        writeToErrorFile(parse_ula.errorMessage)
    #do the semantic analysis if there is no error in the parser
    else:
        parse_ula.writeToFile()
        semanticAnalysis(file)

#####################
# SEMANTIC ANALYSIS #
#####################
def semanticAnalysis(file):
    words = file.split('.')
    f = open(words[0] + ".ast", 'r')

    isAssignment = False

    for line in f:
        if (isAssignment):
            ID = line.split(',')
            if (addVarToList(ID[1]) == False):
                print("error")
            isAssignment = False
        if (line.strip() == "AssignStatement"):
            isAssignment = True

##################################################
# ADD NEW VARIABLE NAME TO THE LIST OF VARIABLES #
##################################################
def addVarToList(var):
    if(checkForVarInList(var)):
        return False
    else:
        global varArray
        varArray.append(var)
        return True

#########################################################
# CHECK IF VARIABLE IS IN THE LIST OF CREATED VARIABLES #
#########################################################
def checkForVarInList(var):
    if (var in varArray):
        return True
    else:
        return False

#####################################
# WRITE THE ERROR TO THE ERROR FILE #
#####################################
def writeToErrorFile(errorMessage):
    #open the file
    words = fileName.split('.')
    f = open(words[0] + ".err", 'w')
    f.write(errorMessage)
    f.close()

#RUN MAIN
if __name__ == '__main__':
    readFromFile(fileName)
    runLexer (fileName)