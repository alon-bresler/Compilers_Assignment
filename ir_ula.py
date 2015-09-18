from llvmlite import ir
from ctypes import CFUNCTYPE, c_float, c_double
import llvmlite.binding as llvm

import ir_parser
import sys


# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

#tree = ["Program", ["=", ["b"], ["@", ["1"], ["2"]]]] # compact ast
last_var = "" # keeps track of the last var assigned
var_dict = {}  # var names associated with memory location
firstPass = True

llvm_ir = """
   ; ModuleID = "examples/ir_fpadd.py"
   target triple = "unknown-unknown-unknown"
   target datalayout = ""

   define double @"fpadd"(double %".1", double %".2")
   {
   entry:
     %"res" = fadd double %".1", %".2"
     ret double %"res"
   }
   """

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod


engine = create_execution_engine()
mod = compile_ir(engine, llvm_ir)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("fpadd")

# Run the function via ctypes
cfunc = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)
res = cfunc(1.0, 3.5)
#print("fpadd(...) =", res)                                                             ## taken out for now

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

#RUN MAIN
if __name__ == '__main__':

    result = ir_parser.readFromFile(sys.argv[1])
    global fileName
    fileName = sys.argv[1]

    flttyp = ir.FloatType() # create float type
    fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
    module = ir.Module(name="ula") # create module named "ula"                              ## compilation unit --> defines set of related functions, global vairables and metadata.
    func = ir.Function(module, fnctyp, name="main") # create "main" function
    block = func.append_basic_block(name="entry") # create block "entry" label              ## the basic block the builder is oeprating on ##
    builder = ir.IRBuilder(block) # create irbuilder to generate code                       ## fill the basic blocks with LLVM instructions || has pointer to block's list of instructions
                                                                                            ## starts at the end of basic block
    #tree.insert(0, "Program")
    #tree = ['Program'].append(tree)
    tree = ['Program']
    tree.append(result)
    code_gen(tree) # call code_gen() to traverse tree & generate code
    builder.ret(builder.load(var_dict[last_var])) # specify return value
    writeToFile(module)