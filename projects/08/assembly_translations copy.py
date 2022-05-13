import sys
file_name = sys.argv[1].split(".")[0].split("/")[-1]

arithmetic = """
@SP
AM=M-1
D=M
A=A-1
M=M.D
"""

bit_stuff = """
@SP
A=M-1
M=.M
"""

logic = """
@SP
AM=M-1
D=M
A=A-1
D=D-M
@zero
D;JEQ
@end
D=0;JMP
(zero)
D=-1
(end)
@SP
A=M-1
M=D
"""

## makes replacements specific to the func ##
math_table = {"add": arithmetic.replace(".", "+"),
              "sub": arithmetic.replace(".", "-"),
              "and": arithmetic.replace(".", "&"),
              "or": arithmetic.replace(".", "|"),
              "not": bit_stuff.replace(".", "!"),
              "neg": bit_stuff.replace(".", "-"),
              "eq": logic,
              "lt": logic.replace("JEQ", "JLT"),
              "gt": logic.replace("JEQ", "JGT")}

symbol_table = {
    "argument": "ARG",
    "local": "LCL",
    "static": 16,
    "constant": 0,
    "this": "this",
    "that": "that",
    "pointer": 3,
    "temp": 5,
}

pop1 = """
@one
D=AorM
@num
D=DandA
"""
pop2 = """
@SP
AM=M-1
D=D+M
A=D-M
M=D-A
"""
push1 = """
@one
D=AorM
@num
A=D+A
D=M
"""
push2 = """
@SP
M=M+1
A=M-1
M=D
"""


def pop_help(str, one, AorM, DandA):
    # makes asm code @ to the right location and do the right opperations
    return str.replace("one", one).replace("AorM", AorM).replace("DandA", DandA)


def push_help(str, one, AorM):
    # makes asm code @ to the right location and do the right opperations
    return str.replace("one", one).replace("AorM", AorM)


# replacements genaric to location
pop_table = {"local": pop_help(pop1, "LCL", "M", "D+A")+pop2,
             "argument": pop_help(pop1, "ARG", "M", "D+A")+pop2,
             "this": pop_help(pop1, "THIS", "M", "D+A") + pop2,
             "that": pop_help(pop1, "THAT", "M", "D+A")+pop2,
             "pointer": pop_help(pop1, str(symbol_table["pointer"]), "A", "D+A")+pop2,
             "temp": pop_help(pop1, str(symbol_table["temp"]), "A", "D+A")+pop2,
             "static": pop_help(pop1, file_name+".num", "A", "D+A")+pop2,
             "constant": pop1.replace("@one\n", "").replace("D=AorM\n", '').replace("DandA", "A")+pop2}

push_table = {"local": push_help(push1, "LCL", "M") + push2,
              "argument": push_help(push1, "ARG", "M") + push2,
              "this": push_help(push1, "THIS", "M") + push2,
              "that": push_help(push1, "THAT", "M") + push2,
              "pointer": push_help(push1, str(symbol_table["pointer"]), "A") + push2,
              "temp": push_help(push1, str(symbol_table["temp"]), "A") + push2,
              "static": push_help(push1, file_name+".num", "A") + push2,
              "constant": "@num\nD=A" + push2}

prog_flow_table = {"label": "(func_name$c)\n",
                   "goto": "@func_name$c\n0;JMP\n",
                   "if-goto": """@SP\nM=M-1\nA=M+1\nD=M+1\n@func_name$c\nD;JNE\n"""}


function = """
// sudo code
// (f)
//      repeat k times:
//      push 0
(FunctionName)             // replace
@num
D=A+1
@R15
M=D
(FunctionName_loop)         // replace
    @R15
    M=M-1
    D=M

    @FunctionName_end       // replace
    D;JEQ               // check if we've pushed n vars

    @0
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

    @FunctionName_loop      // replace
    0;JMP
(FunctionName_end)          // replace

"""

call = """
// #sudo code#
// push return-address
@return_address         // replace
D=A
@SP
M=M+1
A=M-1
M=D

// push LCL
@LCL
D=M
@SP
M=M+1
A=M-1
M=D

// push ARG
@ARG
D=M
@SP
M=M+1
A=M-1
M=D

// push THIS
@THIS
D=M
@SP
M=M+1
A=M-1
M=D

// push THAT
@THAT
D=M
@SP
M=M+1
A=M-1
M=D

// ARG = SP-n-5

@SP
D=M
@num            // replace
D=D-A
@5
D=D-A
@ARG
M=D

// LCL = SP
@SP
D=M
@LCL
M=D

// goto f
@FunctionName        // replace
0;JMP

(return_address)    // replace
"""

returnme = """
// sudo code * means M = *(A)
// FRAME = LCL
@LCL
D=M
@R13
M=D

// RET = *(FRAME-5)
@5
D=D-A
A=D
D=M
@R14
M=D

// *ARG = pop()
@SP
AM=M-1
D=M
@ARG
A=M
M=D

// SP = ARG +1
@ARG
D=M+1
@SP
M=D

// THAT = *(FRAME-1)
@R13
A=M-1
D=M
@THAT
M=D

// THIS = *(FRAME-2)
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D

// ARG = *(FRAME-3)
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D

// LCL = *(FRAME-4)
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D

// got RET
@R14
A=M
0;JMP
"""

subroutine_table = {"function": function, "call": call, "return": returnme}
