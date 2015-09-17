__author__ = 'Alon'

import sys
import lex_ula
import parse_ula

fileName = 'ula_error_samples/testError.ula'

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
    writeToErrorFile(lex_ula.errorMessage)

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