'''
two files: funcs, main

FUNCS
- clean up file
- all funcs [add, sub, neg, eq, gt, lt, and, or, not]
- push pop funcs

MAIN: takes a set of .vm files and translates each into seperate hack .asm files
- seperates files (for file in list)
- cleans the files
'''
'''
check vm file
push/pop thign num within range
'''
'''
python3 VMtranslator.py FunctionCalls/FibonacciElement
python3 VMtranslator.py FunctionCalls/SimpleFunction
python3 VMtranslator.py FunctionCalls/NestedCall/
python3 VMtranslator.py FunctionCalls/StaticsTest/
python3 VMtranslator.py ProgramFlow/BasicLoop/
python3 VMtranslator.py ProgramFlow/FibonacciSeries/
'''


import os
import sys
import VM_parser
import VM_FUNcs
file = sys.argv[1]
files = []
filenames = []
asm_name = file.removesuffix(".vm")

print(f"Finding files to translate...")
for thing in os.listdir(file):
    if thing == "Sys.vm":
        print(f'File: {os.path.join(file, thing)} cued for translating')
        files.append(os.path.join(file, thing))
        filenames.append(thing.removesuffix('.vm'))

for thing in os.listdir(file):
    if thing.endswith(".vm") and not(thing == "Sys.vm"):
        print(f'File: {os.path.join(file, thing)} cued for translating')
        files.append(os.path.join(file, thing))
        filenames.append(thing.removesuffix('.vm'))


print(f"Cleaning files...")
files = [VM_parser.clean(file) for file in files]


def translate(contents, linenum=0, current_func=""):
    program = []
    # print(f'contents {contents}')
    for i, line in enumerate(contents):       # line = push/pop/add/etc.
        print(f"{i+1} of {len(contents)}")
        prog_line = ""
        program.append(f"\n //{line}  \n")
        # line = add/sub/neg/etc.
        if line in [['add'], ['sub'], ['and'], ['or'], ['not'], ['neg'], ['eq'], ['lt'], ['gt']]:
            # get vm to asm translation
            prog_line = VM_FUNcs.translate_math(line[0], linenum)
            # add to program
            program.append(prog_line)
        elif line[0] == "push" or line[0] == "pop":        # line = push or pop
            # get vm to asm translation
            prog_line = VM_FUNcs.translate_pop_push(line)
            # add to program
            program.append(prog_line)
        elif line[0] == "label" or line[0] == "if-goto" or line[0] == "goto":
            prog_line = VM_FUNcs.translate_prog_flow(line, current_func)
            program.append(prog_line)
        elif line[0] == "function" or line[0] == "call" or line[0] == "return":
            if line[0] == "call":
                current_func = line[1]
            if line[0] == "return":
                current_func = ""
            prog_line = VM_FUNcs.translate_subroutine(
                line, linenum)
            program.append(prog_line)
        else:
            print(f"{line} is not a valid command")
            return
        linenum += 1
    return program


def main():
    full_program = []
    linenum = 0
    for i, file in enumerate(files):
        print(f"Translating {filenames[i]}...")
        tranlation = translate(file, linenum, filenames[i])
        for line in tranlation:
            full_program.append(line)
    VM_parser.write_to_file(full_program, asm_name)


main()
