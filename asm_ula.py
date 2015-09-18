import llvmlite.binding as llvm

__author__ = 'Alon'

import ir_ula
import run_ula
import sys

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

#######################
# READ IN THE IR FILE #
#######################
def readInIRFile(file):
    words = file.split('.')
    f = open(words[0] + ".ir", 'r')
    global llvm_ir
    llvm_ir = ""
    for line in f:
        llvm_ir = llvm_ir + line

###########################
# WRITE OUT ASSEMBLY CODE #
###########################
def writeToFile(m):
    #open the file
    words = fileName.split('.')
    f = open(words[0] + ".asm", 'w')
    f.write(str(m))
    f.close()

#RUN MAIN
if __name__ == '__main__':

    global fileName
    fileName = sys.argv[1]
    #fileName = 'ula_irrun_samples/add.ula'
    ir_ula.createIntermediateRepresentation(fileName)
    readInIRFile(fileName)

    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()

    asm = llvm.TargetMachine.emit_assembly(target_machine, mod)

    writeToFile(asm)