__author__ = 'Alon'

import ply.lex as lex

# List of token names #
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN', 'ID', 'COMMENT')

# Regular expression rules for tokens #
t_PLUS      =   r'\@'
t_MINUS     =   r'\$'
t_TIMES     =   r'\#'
t_DIVIDE    =   r'\&'
t_EQUALS    =   r'\='
t_LPAREN    =   r'\('
t_RPAREN    =   r'\)'
t_ignore_COMMENT = r'\//.*' # ignore the comment
#t_ignore_COMMENT = r'\/*.*/*' # ignore the comment

# Regular expression for ID #
def t_ID(t):
    r'_[a-zA-Z][a-zA-Z0-9]*_' #id must start and end with a _
    return t

# A regular expression rule with some action code #
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers #
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs) #
t_ignore  = ' \t'

# Error handling rule #
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer #
lexer = lex.lex()

# Test it out
data = '_TESTID_ = ((2 @ 8) # 10) &20 //test comment'

# Give the lexer some input
lexer.input(data)

# Tokenize
print("TOKENS:")
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    #print(tok)
    print(tok.type, tok.value, tok.lineno, tok.lexpos)

#RUN MAIN
if __name__ == '__main__':
    print("This is now running")