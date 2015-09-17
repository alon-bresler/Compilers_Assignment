from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

tree = ["Program", ["=", ["a"], ["@", ["111"], ["2"]]]] # compact ast
last_var = "" # keeps track of the last var assigned
var_dict = {}  # var names associated with memory location

def code_gen(tree): # traverse tree recursively to generate code
    global last_var
    if tree[0] == "Program":
        for t in tree[1:]:
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
    elif tree[0].isnumeric():
        return(ir.Constant(ir.FloatType(), float(tree[0])))


flttyp = ir.FloatType() # create float type
fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
module = ir.Module(name="ula") # create module named "ula"                              ## compilation unit --> defines set of related functions, global vairables and metadata.
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label              ## the basic block the builder is oeprating on ##
builder = ir.IRBuilder(block) # create irbuilder to generate code                       ## fill the basic blocks with LLVM instructions || has pointer to block's list of instructions
                                                                                        ## starts at the end of basic block
code_gen(tree) # call code_gen() to traverse tree & generate code
builder.ret(builder.load(var_dict[last_var])) # specify return value
print(module)