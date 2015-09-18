from llvmlite import ir
from ctypes import CFUNCTYPE, c_float, c_double
import llvmlite.binding as llvm

import ir_parser
import sys

#tree = ["Program", ["=", ["b"], ["@", ["1"], ["2"]]]] # compact ast
last_var = "" # keeps track of the last var assigned
var_dict = {}  # var names associated with memory location
firstPass = True

######################################################
# RETURN WHETHER THE STRING IS A FLOAT/NUMBER OR NOT #
######################################################
def isFloat(string):
    try:
        float(str(string))
        return True
    except ValueError:
        return False

##############################################
# TRAVERSE TREE RECURSIVELY TO GENERATE CODE #
##############################################
def code_gen(tree):
    global last_var
    if tree[0] == "Program":
        for t in tree[1][0:]:
            code_gen(t)
    elif tree[0] == "=":
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.FloatType())                             ## builder.alloca --> statically allocate stack slot for size va;ues of type typ.
        builder.store(code_gen(tree[2]), var_dict[last_var])                            ## buidler.store --> Store value to pointer ptr
    elif tree[0] == "@":
        return(builder.fadd(code_gen(tree[1]),code_gen(tree[2])))                       ## builder.fadd --> floating-point added to LHS and RHS
    elif tree[0] == "$":
        return(builder.fsub(code_gen(tree[1]),code_gen(tree[2])))                       ## buidler.fsub --> floating-point subtract RHS from LHS
    elif tree[0] == "#":
        return(builder.fmul(code_gen(tree[1]),code_gen(tree[2])))                       ## builder.fmul --> floating-point multiply LHS with RHS
    elif tree[0] == "&":
        return(builder.fdiv(code_gen(tree[1]),code_gen(tree[2])))                       ## builder.fdiv --> floating-point divide LHS by RHS
    #elif tree[0].isnumeric():
    elif isFloat(tree[0]):
        return(ir.Constant(ir.FloatType(), float(tree[0])))
    else:
        return (builder.load(var_dict[tree[0]]))

###########################################
# WRITE THE GENERATED CODE TO THE IF FILE #
###########################################
def writeToFile(m):
    #open the file
    words = fileName.split('.')
    f = open(words[0] + ".ir", 'w')
    f.write(str(m))
    f.close()

def getModule():
    return module

def createIntermediateRepresentation(arg):

    result = ir_parser.readFromFile(arg)
    global fileName
    fileName = arg

    flttyp = ir.FloatType() # create float type
    fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
    global module
    module = ir.Module(name="ula") # create module named "ula"                              ## compilation unit --> defines set of related functions, global vairables and metadata.
    func = ir.Function(module, fnctyp, name="main") # create "main" function
    block = func.append_basic_block(name="entry") # create block "entry" label              ## the basic block the builder is oeprating on ##
    global builder
    builder = ir.IRBuilder(block) # create irbuilder to generate code                       ## fill the basic blocks with LLVM instructions || has pointer to block's list of instructions
                                                                                            ## starts at the end of basic block
    #tree.insert(0, "Program")
    #tree = ['Program'].append(tree)
    tree = ['Program']
    tree.append(result)
    code_gen(tree) # call code_gen() to traverse tree & generate code
    builder.ret(builder.load(var_dict[last_var])) # specify return value
    writeToFile(module)


#RUN MAIN
if __name__ == '__main__':
    createIntermediateRepresentation(sys.argv[1])