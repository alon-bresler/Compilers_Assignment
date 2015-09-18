from __future__ import print_function
from ctypes import CFUNCTYPE, c_double, c_float
import llvmlite.binding as llvm

import ir_ula
import sys


# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

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

def readInIRFile(file):
    words = file.split('.')
    f = open(words[0] + ".ir", 'r')
    global llvm_ir
    llvm_ir = ""
    for line in f:
        llvm_ir = llvm_ir + line

def writeToFile(m):
    #open the file
    words = fileName.split('.')
    f = open(words[0] + ".run", 'w')
    f.write(str(m))
    f.close()


#RUN MAIN
if __name__ == '__main__':

    global fileName
    #fileName = sys.argv[1]
    fileName = 'ula_irrun_samples/add.ula'
    ir_ula.createIntermediateRepresentation(fileName)
    readInIRFile(fileName)

    engine = create_execution_engine()
    mod = compile_ir(engine, llvm_ir)

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address("main")

    # Run the function via ctypes
    cfunc = CFUNCTYPE(c_float)(func_ptr)
    res = cfunc()
    writeToFile(res)
