__author__ = 'Alon'

import sys
import lex_ula
import parse_ula

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


#RUN MAIN
if __name__ == '__main__':
    readFromFile('ula_error_samples/testError.ula')
    runLexer ('ula_error_samples/testError.ula')