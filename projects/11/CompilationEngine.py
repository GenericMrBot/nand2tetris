from importlib.metadata import files
import os
import sys
import Tokenizer
import JackCompiler

jfolder = sys.argv[1]


def CompileFile(file, classNames):
    return


def que(jfolder):
    '''
    args: jfolder (folder or jack file) 
    outputs: (list) of paths to all jack files in the folder
    '''
    qfiles = []
    filenames = []
    print(f"queing files...")

    if jfolder[-5:] == ".jack":
        print(f'File: {jfolder}, cued for compiling')
        return [jfolder]

    for thing in os.listdir(jfolder):
        if thing.endswith(".jack"):
            print(f'File: {os.path.join(jfolder, thing)}, cued for compiling')
            qfiles.append(os.path.join(jfolder, thing))
            filenames.append(thing.removesuffix('.jack'))
    return qfiles


def write_to_file(text, filename):
    with open(filename, "w") as file:
        file.write(text)


def main(jfolder):
    '''
    args: jfolder (folder or jack file)
    returns: xml file
    '''

    qfiles = que(jfolder)
    classNames = [file.split("/")[-1].split(".")[0] for file in qfiles]
    for file in qfiles:
        tokens, lexLabels = Tokenizer.Tokenizer(file)
        xmlfile = JackCompiler.JackCompiler(
            tokens, lexLabels, file, classNames)
        xmlfile.Compile()
        xmlfile.writeVM()


main(jfolder)
