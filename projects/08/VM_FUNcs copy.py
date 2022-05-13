''' info about how I'm doing the math operations
# add ### replace . with + for add, - for sub, & for and, | for or
@SP
AM=M-1
D=M
A=A-1
M=D.M

# Neg ### replace . with ! for not, - for neg
@SP
A=M-1
M=.M

# eq lt gt ### replace JEQ with JEQ for eq, JLT for lt, JGT for gt
@SP
A=M-1
D=M         // x
A=A-1
D=D-M       // x-y
@jump
D;JEQ       // jump if x-y lt, gt, eq to 0
@end
D=0;JMP
(zero)
D=-1
(end)
@SP
AM=M-1
A=A-1
M=D

'''
''' Push Pop Stuff
### POP ###
@{symbol_table[line[1]]}
D=M
@{line[2]}
D=D+A
@SP
AM=M-1
D=D+M
A=D-M
M=D-A
### PUSH ###
@{symbol_table[line[1]]}

'''
''' Program flow stuff
label c
(func_name$c)

goto c
@func_name$c
0;JMP

if-goto c
@SP
AM=M-1
D=M     /D=-1 if prev statement = true, 0 if false
@func_name$c
D;JEQ

'''
''' Subroutine calling stuff
function g nVars
- make label
-

call g nArgs
- save in order: return address, lcl, arg, this, that, arg=sp-n-5, lcl = sp, goto f

return
-
'''




import VM_parser
from assembly_translations import *
def translate_math(line, linenum):
    '''
    Arguements:
        line: str, vm command
        linenum: int, line number for jump cmd names
    returns:
        the assembly translaiton of the input command
    '''
    return math_table[line].replace("end", f"end.{linenum}").replace("zero", f"zero.{linenum}")


def translate_pop_push(line):
    prog_lines = ""
    if line[0] == "pop":
        # check if temp or pointer goes out of 5-12 and 3-4 RAM loc
        if line[1] == "temp" and int(line[2]) > 8:
            # I know this isn't the right way to raise an error but it works
            print("temp out of range")
            raise
        if line[1] == "pointer" and int(line[2]) > 2:
            print("pointer out of range")
            raise
        prog_lines = pop_table[line[1]].replace("num", str(line[2]))
    elif line[0] == "push":
        # check if temp or pointer goes out of 5-12 and 3-4 RAM loc
        if line[1] == "temp" and int(line[2]) > 8:
            print("temp out of range")
            raise
        if line[1] == "pointer" and int(line[2]) > 2:
            print("pointer out of range")
            raise
        prog_lines = push_table[line[1]].replace("num", str(line[2]))
    return prog_lines


def translate_prog_flow(line, funcname):
    return prog_flow_table[line[0]].replace("func_name$c", f"{funcname}${line[1]}")


def translate_subroutine(line, linenum):
    prog_lines = VM_parser.clean_assembly(subroutine_table[line[0]])
    if line[0] == "function":
        prog_lines = "\n".join(prog_lines).replace(
            "FunctionName", line[1]).replace(
            "num", line[2]) + "\n"
    elif line[0] == "call":
        prog_lines = "\n".join(prog_lines).replace(
            "FunctionName", line[1]).replace(
            "num", line[2]).replace(
            "return_address", "return_address" + str(linenum)) + "\n"
    elif line[0] == "return":
        prog_lines = "\n".join(prog_lines) + "\n"
    return prog_lines
