import llvmlite.binding as llvm

__author__ = 'Alon'

import ir_ula
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
# WRITE OUT RESULT OF RUN #
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
    #fileName = sys.argv[1]
    fileName = 'ula_irrun_samples/add.ula'
    ir_ula.createIntermediateRepresentation(fileName)
    readInIRFile(fileName)

    #llvm_module = llvm.parse_assembly(llvm_ir)
    #tm = llvm.Target.from_default_triple().create_target_machine()
    #engine = llvm.create_mcjit_compiler(llvm_module, tm)
    #engine.finalize_object()
    #print(llvm_module)
    print(ir_ula.getModule())
    asm = llvm.TargetMachine.emit_assembly(ir_ula.getModule())
    print(asm)