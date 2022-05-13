
def clean_assembly(str):
    '''
    Args: string of assembly funcs
    returns: list of assembly lines with removed comments,
                blank lines, and new lines
    notes: still has placeholders
    '''
    str = str.split("\n")
    contents = [lines.split("//")[0]
                for lines in str]      # removes comments
    contents = [lines.strip()
                for lines in contents]      # removes new lines
    contents = [lines for lines in contents if len(
        lines) > 0]                         # removes blank lines
    # print(f'contents {contents}')
    return contents


def clean(file):
    thing = file.split(".")[-1]
    if thing == "vm":
        with open(file, "r") as file:
            contents = file.readlines()
        contents = [lines.split("//")[0]
                    for lines in contents]      # removes comments
        contents = [lines.strip()
                    for lines in contents]      # removes new lines
        contents = [lines for lines in contents if len(
            lines) > 0]                         # removes blank lines
        contents = [lines.split()
                    for lines in contents]     # gets rid of white space
        return contents
    raise "file doesn't have vm suffix"


def write_to_file(program, file):
    if file[-3:] == ".vm":
        filename = file[:-3] + ".asm"  # change file.vm to file.asm
    else:
        file = file.removesuffix("/")
        filename = file + "/" + file.split("/")[-1] + ".asm"
    with open(filename, "w") as thing:
        for line in program:
            thing.write(line)              # write to file
    print(f"{filename} contains the assembly translation")
